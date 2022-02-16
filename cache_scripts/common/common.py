from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict
import logging
import json

import pandas as pd

with open(Path('cache_scripts') / 'endpoints.json') as json_file:
    ENDPOINTS: Dict = json.load(json_file)

class Collector(ABC):
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
            df.reset_index().to_feather(self.data_path)
            return

        prev_df: pd.DataFrame = pd.read_feather(self.data_path)

        # If force is selected, we delete the ones of the same network only
        if force:
            prev_df = prev_df[prev_df["network"] != self.network]
        
        prev_df.set_index(['id', 'network'], inplace=True, verify_integrity=True)
        df.set_index(['id', 'network'], inplace=True, verify_integrity=True)

        # Updating data
        combined = df.combine_first(prev_df).reset_index()
        combined.to_feather(self.data_path)
        return combined

    @abstractmethod
    def run(self, force=False, **kwargs) -> None:
        return

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