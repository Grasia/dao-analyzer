from typing import List
import pandas as pd
from pathlib import Path

from src.apps.common.data_access.requesters.irequester import IRequester

class CacheRequester(IRequester):
    def __init__(self, srcs: List[Path]):
        self.__srcs = srcs

    # TODO: Add memoization using the metadata.json file
    def request(self, *args) -> pd.DataFrame:
        """
        Gets data from datawarehouse.
        Arguments:
            * args: Its not used
        Return:
            a pandas dataframe with all the data loaded. If the src does not 
            exist, it will return an empty dataframe.
        """
        df: pd.DataFrame = pd.DataFrame()
        for src in self.__srcs:
            if src.is_file():
                df = pd.concat([df, pd.read_feather(src)], axis=0, ignore_index=True)
        
        return df
