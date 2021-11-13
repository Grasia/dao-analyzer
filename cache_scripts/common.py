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

from api_requester import ApiRequester

with open(Path('cache_scripts') / 'endpoints.json') as json_file:
    ENDPOINTS: Dict = json.load(json_file)

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

    def verify(self) -> bool:
        """
        Checks if the Collector is in a valid state. This check is run for every
        collector before starting to get data. Can be ignored with --no-verify
        """
        return True

    @abstractmethod
    def run(self, force=False) -> None:
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

    def run(self, force=False):
        # TODO: Check if meta version is not good, force = true

        # open last df if exists and get last_index
        # TODO: This won't work. They are sorted by increasing id
        # which means that the latest received item is an 0xffff...
        # The last_index method only serves for pagination, a new item could
        # appear with an id less than the max one, and we wouldn't detect it
        # we have to use the creation date or something like that
        last_index: str = "0x0"
        prev_df: pd.DataFrame = pd.DataFrame()
        ## TODO: Force with -n mainnet will also erase the xdai data
        ## Is this what we want?
        if not force and self.data_path.is_file():
            prev_df: pd.DataFrame = pd.read_feather(self.data_path)
            last_index = prev_df[self.index][prev_df['network'] == self.network].max()
            if pd.isna(last_index):
                last_index: str = "0x0"

        ## TODO: Catch keyboard interrupt and save whatever we have downloaded
        # We would need to save on the metadata the block number or something so
        # new items don't appear between the ids. Alternative: Dont save anything
        data: List[Dict] = self.requester.n_requests(
            query=self.query,
            index=self.index,
            result_key=self.result_key,
            last_index=last_index)

        # transform to df
        df: pd.DataFrame = self.transform_to_df(data)
        for post in self.postprocessors:
            df = post(df)
            if df is None:
                raise ValueError(f"The postprocessor {post.__name__} returned None")

        if df.empty:
            logging.warning("Empty dataframe, not updating file")
            return

        df = prev_df.append(df).reset_index(drop=True)

        # rewrite df to file
        df.to_feather(self.data_path)

class Runner(ABC):
    def __init__(self):
        self.basedir: Path = Path('datawarehouse') / self.name
        self.networks = {n for n,v in ENDPOINTS.items() if self.name in v}

    @property
    def collectors(self) -> List[Collector]:
        return []

    def run(self, networks: List[str] = [], force=False, collectors=None):
        self.basedir.mkdir(parents=True, exist_ok=True)

        print(f'--- Updating {self.name} datawarehouse ---')

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

        if not verified:
            print("Not running any collectors, available collectors are:")
            print(", ".join([c.long_name for c in self.collectors]))

        for c in verified:
            print(f"Running collector {c.long_name} ({c.network})")
            c.run(force)

        print(f'--- {self.name}\'s datawarehouse updated ---')