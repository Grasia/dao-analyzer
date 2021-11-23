"""
    Descp: Common pieces for data retrieval scripts

    Created on: 02-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""

from pathlib import Path
from abc import ABC, abstractmethod
from gql.dsl import DSLField
from typing import Callable, Dict, List
import json
import pandas as pd
import logging

import config
from api_requester import ApiRequester
from metadata import RunnerMetadata, Block

with open(Path('cache_scripts') / 'endpoints.json') as json_file:
    ENDPOINTS: Dict = json.load(json_file)

def add_where(d, **kwargs):
    if "where" in d:
        d["where"] |= kwargs
    else:
        d["where"] = kwargs
    
    return d

class Collector(ABC):
    def __init__(self, name:str, runner):
        self.name: str = name
        self.runner_name: str = runner.name

    @property
    def data_path(self) -> Path:
        return Path('datawarehouse') / self.runner_name / (self.name + '.arr')

    @property
    def long_name(self) -> str:
        return f"{self.runner_name}/{self.name}"
    
    @property
    def df(self) -> pd.DataFrame:
        return pd.DataFrame()

    def verify(self) -> bool:
        """
        Checks if the Collector is in a valid state. This check is run for every
        collector before starting to get data. Can be ignored with --no-verify
        """
        return True

    @abstractmethod
    def run(self, force=False, **kwargs) -> None:
        return

class GraphQLCollector(Collector):
    def __init__(self, name: str, runner, endpoint: str, result_key: str = None, index: str = None, network: str='mainnet', pbar_enabled: bool=True):
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
    def schema(self):
        return self.requester.get_schema()

    @abstractmethod
    def query(self, **kwargs) -> DSLField:
        raise NotImplementedError

    @property
    def df(self) -> pd.DataFrame:
        df = pd.read_feather(self.data_path)
        if self.network:
            df = df[df['network'] == self.network]
        
        return df

    def transform_to_df(self, data: List[Dict]) -> pd.DataFrame:
        # TODO: Consider the schema to put column names even in empty dataframes
        df = pd.DataFrame.from_dict(pd.json_normalize(data))

        # For compatibility reasons we change from . to snake case
        def dotsToSnakeCase(str: str) -> str:
            splitted = str.split('.')
            return splitted[0] + ''.join(x[0].upper()+x[1:] for x in splitted[1:])
                        
        df.rename(columns=dotsToSnakeCase, inplace=True)
        df['network'] = self.network
        return df

    def verify(self) -> bool:
        self.query()
        return True

    def _update_data(self, df: pd.DataFrame, force: bool = False):
        if df.empty:
            logging.warning("Empty dataframe, not updating file")
            return

        if not self.data_path.is_file():
            df.to_feather(self.data_path)
            return

        prev_df: pd.DataFrame = pd.read_feather(self.data_path)

        # If force is selected, we delete the ones of the same network only
        if force:
            prev_df = prev_df[prev_df["network"] != self.network]
        
        prev_df.set_index(['id', 'network'], inplace=True, verify_integrity=True)
        df.set_index(['id', 'network'], inplace=True, verify_integrity=True)

        # TODO: Add backup thing

        # Updating data
        df.combine_first(prev_df).reset_index().to_feather(self.data_path)

    def run(self, force=False, block: Block = None):
        # TODO: Check if meta version is not good, force = true

        # open last df if exists and get last_index
        # TODO: This won't work. They are sorted by increasing id
        # which means that the latest received item is an 0xffff...
        # The last_index method only serves for pagination, a new item could
        # appear with an id less than the max one, and we wouldn't detect it
        # we have to use the creation date or something like that
        if block is None:
            block = Block()

        ## TODO: Catch keyboard interrupt and save whatever we have downloaded
        # We would need to save on the metadata the block number or something so
        # new items don't appear between the ids. Alternative: Dont save anything
        data: List[Dict] = self.requester.n_requests(
            query=self.query,
            index=self.index,
            block_hash=block.id)

        # transform to df
        df: pd.DataFrame = self.transform_to_df(data)
        for post in self.postprocessors:
            df = post(df)
            if df is None:
                raise ValueError(f"The postprocessor {post.__name__} returned None")

        self._update_data(df, force)

class Runner(ABC):
    def __init__(self):
        self.basedir: Path = Path('datawarehouse') / self.name
        self.networks = {n for n,v in ENDPOINTS.items() if self.name in v}

    @property
    def collectors(self) -> List[Collector]:
        return []

    @staticmethod
    def validated_block(network: str, number_gte: int = 0) -> Block:
        requester = ApiRequester(ENDPOINTS[network]["_blocks"])
        ds = requester.get_schema()
        return Block(requester.request(ds.Query.blocks(
            first=1,
            skip=config.SKIP_INVALID_BLOCKS,
            orderBy="number",
            orderDirection="desc",
            where={"number_gte": number_gte}
        ).select(
            ds.Block.id,
            ds.Block.number,
            ds.Block.timestamp
        ))["blocks"][0])

    def run(self, networks: List[str] = [], force=False, collectors=None):
        self.basedir.mkdir(parents=True, exist_ok=True)

        tocheck = [c for c in self.collectors if (not collectors or c.long_name in collectors) and
                                                 c.network in networks]

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

        if verified:
            # TODO: What if someone presses CTRL+C and there are some collectors
            # still to be run?
            # TODO: Ignore errors (but save them in the metadata)
            with RunnerMetadata(self) as metadata:
                print(f'--- Updating {self.name} datawarehouse ---')            
                blocks: dict[str, Block] = {}
                for c in verified:
                    if c.network not in blocks:
                        # Getting a block more recent than the one in the metadata
                        metadata[c.network].block = blocks[c.network] = self.validated_block(c.network, metadata[c.network].block.number)
                    print(f"Running collector {c.long_name} ({c.network}) on block {blocks[c.network].id[:15]}...")
                    c.run(force, blocks[c.network])
                print(f'--- {self.name}\'s datawarehouse updated ---')