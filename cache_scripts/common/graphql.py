from typing import Callable, List, Dict, Iterable
from datetime import datetime
import logging
from abc import ABC, abstractmethod
import traceback

import pandas as pd

from gql.dsl import DSLField

from .common import Collector, Runner, ENDPOINTS
from .. import config
from ..api_requester import ApiRequester
from ..metadata import RunnerMetadata, Block

def add_where(d, **kwargs):
    """
    Adds the values specified in kwargs to the where inside d
        Example: `**add_where(kwargs, deleted=False)`
    """
    if "where" in d:
        d["where"] |= kwargs
    else:
        d["where"] = kwargs
    
    return d

def partial_query(q, w) -> DSLField:
    def wrapper(**kwargs):
        return q(**add_where(kwargs, **w))
    return wrapper

class GraphQLCollector(Collector):
    def __init__(self, name: str, runner: Runner, endpoint: str, result_key: str = None, index: str = None, network: str='mainnet', pbar_enabled: bool=True):
        super().__init__(name, runner)
        self.endpoint: str = endpoint
        self.index = index if index else 'id'
        self.result_key = result_key if result_key else name
        self.network = network
        self.postprocessors: Callable = []

        self.requester: ApiRequester = ApiRequester(endpoint=self.endpoint, pbar_enabled=pbar_enabled)

    def postprocessor(self, f: Callable[[pd.DataFrame], pd.DataFrame]):
        self.postprocessors.append(f)
        return f

    @property
    def collectorid(self) -> str:
        return '-'.join([super().collectorid, self.network])

    @property
    def schema(self):
        return self.requester.get_schema()

    @abstractmethod
    def query(self, **kwargs) -> DSLField:
        raise NotImplementedError

    @property
    def df(self) -> pd.DataFrame:
        if not self.data_path.is_file():
            return pd.DataFrame()

        df = pd.read_feather(self.data_path)
        if self.network:
            df = df[df['network'] == self.network]
        
        return df

    def transform_to_df(self, data: List[Dict], skip_post: bool=False) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(pd.json_normalize(data))

        # For compatibility reasons we change from . to snake case
        def dotsToSnakeCase(str: str) -> str:
            splitted = str.split('.')
            return splitted[0] + ''.join(x[0].upper()+x[1:] for x in splitted[1:])
                        
        df.rename(columns=dotsToSnakeCase, inplace=True)
        df['network'] = self.network

        if not skip_post:
            for post in self.postprocessors:
                df = post(df)
                if df is None:
                    raise ValueError(f"The postprocessor {post.__name__} returned None")

        return df

    def verify(self) -> bool:
        self.query()
        return True

    def run(self, force=False, block: Block = None):
        if block is None:
            block = Block()

        data: List[Dict] = self.requester.n_requests(
            query=self.query,
            index=self.index,
            block_hash=block.id)

        # transform to df
        df: pd.DataFrame = self.transform_to_df(data)
        self._update_data(df, force)

class GraphQLUpdatableCollector(GraphQLCollector):
    DEFAULT_START_TEXT = "Updating data since {date}"
    DEFAULT_END_TEXT = "There are {len} new items"

    def run(self, force=False, *args, **kwargs):
        if not force and not self.df.empty:
            self.update(*args, **kwargs)
        else:
            super().run(force, *args, **kwargs)

    def _simple_timestamp(self, key: str = 'createdAt', block: Block = None, start_txt=DEFAULT_START_TEXT, end_txt=DEFAULT_END_TEXT, prev_df: pd.DataFrame = None):
        # 1. Get the max createdAt
        if prev_df is None:
            prev_df = self.df
        
        if prev_df.empty:
            return

        maxCreatedAt = int(prev_df[key].fillna(0).astype(int).max())
        print(start_txt.format(date=datetime.fromtimestamp(maxCreatedAt).isoformat()))

        # 2. Perform n_requests but with bigger createdAt than the max createdAt
        data = self.requester.n_requests(
            query=partial_query(self.query, {f"{key}_gte": maxCreatedAt}),
            block_hash=block.id)

        # 3. Update the file
        df = self.transform_to_df(data)
        print(end_txt.format(len=len(df)))
        self._update_data(df)

    def update(self, block: Block = None):
        self._simple_timestamp('createdAt', block)

class GraphQLRunner(Runner, ABC):
    def __init__(self, dw = None):
        super().__init__(dw)
        self.networks = {n for n,v in ENDPOINTS.items() if self.name in v}

    def filterCollectors(self, 
        networks: Iterable[str] = [],
        names: Iterable[str] = [],
        long_names: Iterable[str] = []
    ) -> Iterable[Collector]:
        # networks ^ (names v long_names)
        result = self.collectors
        if networks:
            result = (c for c in result if c.network in networks)

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
            networks=[network],
            names=[name],
            long_names=[long_name]
        ), None)

    @staticmethod
    def validated_block(network: str, prev_block: Block = None) -> Block:
        requester = ApiRequester(ENDPOINTS[network]["_blocks"])
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
            args["skip"] = 0
            args["where"]["number_gte"] = 0
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
        for c in tocheck:
            try:
                if c.verify():
                    verified.append(c)
                else:
                    print("Verified returned false for {c.long_name} ({c.network})")
            except Exception as e:
                print(f"Won't run {c.long_name} ({c.network})")
                print(e)
        return verified

    def run(self, networks: List[str] = [], force=False, collectors=None):
        self.basedir.mkdir(parents=True, exist_ok=True)

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
                    if c.network not in blocks:
                        # Getting a block more recent than the one in the metadata
                        print("Requesting a block number...", end='\r')
                        blocks[c.network] = self.validated_block(c.network, None if force else metadata[c.collectorid].block)
                        print(f"Using block {blocks[c.network].id} for {c.network} (ts: {blocks[c.network].timestamp.isoformat()})")

                    print(f"Running collector {c.long_name} ({c.network})")
                    olderBlock = blocks[c.network] < metadata[c.collectorid].block
                    if not force and olderBlock:
                        print("Warning: Forcing because requesting an older block")
                        logging.warning("Forcing because using an older block")

                    c.run(force or olderBlock, blocks[c.network])
                    metadata[c.collectorid].block = blocks[c.network]
                except Exception as e:
                    metadata.errors[c.collectorid] = e.__str__()
                    print(traceback.format_exc())
            print(f'--- {self.name}\'s datawarehouse updated ---')