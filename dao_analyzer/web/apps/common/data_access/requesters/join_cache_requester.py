from dao_analyzer.web.apps.common.data_access.requesters.cache_requester import CacheRequester


from typing import List
from pathlib import Path

import pandas as pd

class JoinCacheRequester(CacheRequester):
    """
    A Cache Requester that joins instead of concatenating the dataframes
    """
    
    def __init__(self, srcs: List[Path], on=None, how='outer', dropna=False, columns=None):
        """Initializes the CacheRequester

        Args:
            srcs (List[Path]): A list of paths to read the dfs from
            on: If None, use intersection of columns in all dfs, ignoring the `id`
                column. Defaults to None.
        """
        super().__init__(srcs)
        self._on = on
        self._how = how
        self._dropna = dropna
        self._cols = columns
    
    def tryReload(self):
        dfs = map(pd.read_feather, self._srcs)
        dfs = map(lambda df: df.drop(columns='id'), dfs)

        if self._cols:
            dfs = map(lambda df: df[df.columns.intersection(self._cols)], dfs)

        if self._dropna:
            dfs = map(lambda df: df.dropna(), dfs)

        joined = next(dfs, pd.DataFrame())
        for df in dfs:
            joined = joined.merge(df, how=self._how, on=self._on, suffixes=(None, "_y"))

        self._df = joined