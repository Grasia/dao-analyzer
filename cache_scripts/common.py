"""
    Descp: Common pieces for data retrieval scripts

    Created on: 02-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""

from pathlib import Path
from abc import ABC, abstractmethod
from gql.dsl import DSLField
from typing import Dict, List
import json
import pandas as pd
import logging

from api_requester import ApiRequester

with open(Path('cache_scripts') / 'endpoints.json') as json_file:
    ENDPOINTS: Dict = json.load(json_file)

## TODO: SEPARATE COLLECTOR TO THEGRAPHCOLLECTOR
## THAT WAY; WE CAN CREATE MORE COLLECTORS THAT DONT USE THEGRAPH AS A BACKEND
class Collector(ABC):
    def __init__(self, name:str, runner):
        self.name: str = name
        self.runner_name: str = runner.name

    @property
    def data_path(self) -> Path:
        return Path('datawarehouse') / self.runner_name / (self.name + '.arr')

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
    def __init__(self, name: str, runner, endpoint: str, result_key: str = None, index: str = None):
        super().__init__(name, runner)
        self.endpoint: str = endpoint
        self.index = index if index else 'id'
        self.result_key = result_key if result_key else name

        self.requester: ApiRequester = ApiRequester(endpoint=self.endpoint)
    
    @property
    def schema(self):
        return self.requester.get_schema()

    @abstractmethod
    def query(self, **kwargs) -> DSLField:
        raise NotImplementedError

    def transform_to_df(self, data: List[Dict]) -> pd.DataFrame:
        return pd.DataFrame(data)

    def verify(self) -> bool:
        self.query()
        return True

    def run(self, force=False):
        # TODO: Check if meta version is not good, force = true

        # open last df if exists and get last_index
        last_index: str = ""
        prev_df: pd.DataFrame = None
        if not force and self.data_path.is_file():
            logging.info("Continuing last request")
            prev_df: pd.DataFrame = pd.read_feather(self.data_path)
            last_index = prev_df[self.index].max()

        data: List[Dict] = self.requester.n_requests(
            query=self.query,
            index=self.index,
            result_key=self.result_key,
            last_index=last_index)

        # transform to df
        df: pd.DataFrame = self.transform_to_df(data)

        if df.empty:
            logging.info("Empty dataframe, not updating file")
            return

        print(df)
        if prev_df:
            df = prev_df.concat(df)

        # rewrite df to file
        df.to_feather(self.data_path)

class Runner(ABC):
    def __init__(self):
        self.basedir: Path = Path('datawarehouse') / self.name
        self.networks = {n for n,v in ENDPOINTS.items() if self.name in v}

    @property
    def collectors(self) -> List[Collector]:
        return []

    def run(self, networks: List[str] = [], force=False):
        self.basedir.mkdir(parents=True, exist_ok=True)

        print(f'--- Updating {self.name} datawarehouse ---')

        verified = [c for c in self.collectors if c.verify()]
        # TODO: USE NETWORK
        for n in self.networks.intersection(networks):
            for c in verified:
                c.run(force)

        print(f'--- {self.name}\'s datawarehouse updated ---')