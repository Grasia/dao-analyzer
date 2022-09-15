from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Iterable
import logging
import sys
import json
from datetime import datetime, timezone
import traceback
import pkgutil

from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt
import pandas as pd
from tqdm import tqdm
from gql.transport.exceptions import TransportQueryError

from .api_requester import GQLRequester
from ..metadata import RunnerMetadata, Block
from .. import config
from ... import cache_scripts

# To be able to obtain endpoints.json
ENDPOINTS: Dict = json.loads(pkgutil.get_data(cache_scripts.__name__, 'endpoints.json'))

def solve_decimals(df: pd.DataFrame) -> pd.DataFrame:
    """ Adds the balanceFloat column to the dataframe

    This column is a precalculated value of tokenBalance / 10 ** tokenDecimals as float
    """
    dkey, bkey, fkey = 'decimals', 'balance', 'balanceFloat'

    df[dkey] = df[dkey].astype(int)
    df[fkey] = df[bkey].astype(float) / 10 ** df[dkey]

    return df

class Collector(ABC):
    INDEX = ['network', 'id']
    
    def __init__(self, name:str, runner):
        self.name: str = name
        self.runner = runner

    @property
    def data_path(self) -> Path:
        return self.runner.basedir / (self.name + '.arr')

    @property
    def long_name(self) -> str:
        return f"{self.runner.name}/{self.name}"

    @property
    def collectorid(self) -> str:
        return self.long_name

    @property
    def df(self) -> pd.DataFrame:
        return pd.DataFrame()

    def verify(self) -> bool:
        """
        Checks if the Collector is in a valid state. This check is run for every
        collector before starting to get data. Can be ignored with --no-verify
        """
        return True

    def _update_data(self, df: pd.DataFrame, force: bool = False) -> pd.DataFrame:
        """ Updates the dataframe in `self.data_path` with the new data.
        """
        if df.empty:
            logging.warning("Empty dataframe, not updating file")
            return

        if not self.data_path.is_file():
            df.reset_index(drop=True).to_feather(self.data_path)
            return

        prev_df: pd.DataFrame = pd.read_feather(self.data_path)

        # If force is selected, we delete the ones of the same network only
        if force:
            prev_df = prev_df[prev_df["network"] != self.network]
        
        prev_df = prev_df.set_index(self.INDEX, verify_integrity=True, drop=True)
        df = df.set_index(self.INDEX, verify_integrity=True, drop=True)

        # Updating data
        combined = df.combine_first(prev_df).reset_index()
        combined.to_feather(self.data_path)
        return combined

    @abstractmethod
    def run(self, force=False, **kwargs) -> None:
        return

class NetworkCollector(Collector):
    """ Collector runnable in a specific network and to a block number """
    def __init__(self, name: str, runner, network: str='mainnet'):
        super().__init__(name, runner) 
        self.network = network

    @property
    def collectorid(self) -> str:
        return '-'.join([super().collectorid, self.network])

class UpdatableCollector(Collector): # Flag class
    pass

class Runner(ABC):
    def __init__(self, dw: Path = Path()):
        self.__dw: Path = dw

    def set_dw(self, dw) -> Path:
        self.__dw = dw

    @property
    def basedir(self) -> Path:
        return self.__dw / self.name

    @property
    def collectors(self) -> List[Collector]:
        return []

    def run(self, **kwargs):
        raise NotImplementedError

class NetworkRunner(Runner, ABC):
    def __init__(self, dw = None):
        super().__init__(dw)
        self.networks = {n for n,v in ENDPOINTS.items() if self.name in v and not n.startswith('_')}

    def filterCollectors(self, 
        networks: Iterable[str] = [],
        names: Iterable[str] = [],
        long_names: Iterable[str] = []
    ) -> Iterable[Collector]:
        result = self.collectors

        if config.only_updatable:
            result = filter(lambda c: isinstance(c, UpdatableCollector), result)

        # networks ^ (names v long_names)
        if networks:
            # GraphQLCollector => c.network in networks
            # a => b : not(a) or b
            result = filter(lambda c: not isinstance(c, NetworkCollector) or c.network in networks, result)

        if names or long_names:
            result = (c for c in result if c.name in names or c.long_name in long_names)

        return result

    def filterCollector(self,
        collector_id: str = None,
        network: str = None,
        name: str = None,
        long_name: str = None,
    ) -> Collector:
        if collector_id:
            return next((c for c in self.collectors if c.collectorid == collector_id), None)

        return next(self.filterCollectors(
            networks=[network] if network else [],
            names=[name] if name else [],
            long_names=[long_name] if long_name else []
        ), None)

    @staticmethod
    @retry(retry=retry_if_exception_type(TransportQueryError), wait=wait_exponential(max=10), stop=stop_after_attempt(3))
    def validated_block(network: str, prev_block: Block = None) -> Block:
        requester = GQLRequester(ENDPOINTS[network]["_blocks"])
        ds = requester.get_schema()

        number_gte = prev_block.number if prev_block else 0
        
        args = {
            "first": 1,
            "skip": config.SKIP_INVALID_BLOCKS,
            "orderBy": "number",
            "orderDirection": "desc",
            "where": {
                "number_gte": number_gte
            }
        }

        if config.block_datetime:
            del args["skip"]
            del args["where"]["number_gte"]
            args["where"]["timestamp_lte"] = int(config.block_datetime.timestamp())

        response = requester.request(ds.Query.blocks(**args).select(
            ds.Block.id,
            ds.Block.number,
            ds.Block.timestamp
        ))["blocks"]
    
        if len(response) == 0:
            logging.warning(f"Blocks query returned no response with args {args}")
            return prev_block

        return Block(response[0])

    @staticmethod
    def _verifyCollectors(tocheck: Iterable[Collector]):
        verified = []
        for c in tqdm(list(tocheck), desc="Verifying"):
            try:
                if c.verify():
                    verified.append(c)
                else:
                    print(f"Verified returned false for {c.collectorid} (view logs the see why)")
            except Exception:
                print(f"Won't run {c.collectorid}", file=sys.stderr)
                traceback.print_exc()
        return verified

    def run(self, networks: List[str] = [], force=False, collectors=None):
        self.basedir.mkdir(parents=True, exist_ok=True)

        print("Verifying collectors")
        verified = self._verifyCollectors(self.filterCollectors(
            networks=networks,
            long_names=collectors
        ))
        if not verified:
            # Nothing to do
            return

        with RunnerMetadata(self) as metadata:
            print(f'--- Updating {self.name} datawarehouse ---')            
            blocks: dict[str, Block] = {}
            for c in verified:
                try:
                    if isinstance(c, NetworkCollector):
                        if c.network not in blocks:
                            # Getting a block more recent than the one in the metadata (just to narrow down the search)
                            print("Requesting a block number...", end='\r')
                            blocks[c.network] = self.validated_block(c.network, None if force else metadata[c.collectorid].block)
                            print(f"Using block {blocks[c.network].id} for {c.network} (ts: {blocks[c.network].timestamp.isoformat()})")

                        print(f"Running collector {c.long_name} ({c.network})")
                        olderBlock = blocks[c.network] < metadata[c.collectorid].block
                        if not force and olderBlock:
                            print("Warning: Forcing because requesting an older block")
                            logging.warning("Forcing because using an older block")

                        # Running the collector
                        c.run(
                            force=force or olderBlock, 
                            block=blocks[c.network],
                            prev_block=metadata[c.collectorid].block,
                        )

                        # Updating the block in the metadata
                        metadata[c.collectorid].block = blocks[c.network]
                    else:
                        print(f"Running collector {c.long_name}")
                        c.run(
                            force=force,
                        )

                    metadata[c.collectorid].last_update = datetime.now(timezone.utc)
                except Exception as e:
                    metadata.errors[c.collectorid] = e.__str__()
                    if config.ignore_errors:
                        print(traceback.format_exc())
                    else:
                        raise e
            print(f'--- {self.name}\'s datawarehouse updated ---')