"""
   Descp: This class is used to load data from the datawarehouse.

   Created on: 16-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import pandas as pd
import os
from typing import List

from src.apps.daostack.data_access.requesters.irequester import IRequester

CACHE_PATH: str = os.path.join('datawarehouse', 'daostack')
DAOS: str = os.path.join(CACHE_PATH, 'daos.csv')
PROPOSALS: str = os.path.join(CACHE_PATH, 'proposals.csv')
REP_HOLDERS: str = os.path.join(CACHE_PATH, 'reputation_holders.csv')
STAKES: str = os.path.join(CACHE_PATH, 'stakes.csv')
VOTES: str = os.path.join(CACHE_PATH, 'votes.csv')
ALL_FILES: List[str] = [DAOS, PROPOSALS, REP_HOLDERS, STAKES, VOTES]


class CacheRequester(IRequester):
    def __init__(self, src: str):
        self.__src = src


    def request(self, *args) -> pd.DataFrame:
        """
        Gets data from datawarehouse.
        Arguments:
            * args: Its not used
        Return:
            a pandas dataframe with all the data loaded. If the src does not 
            exist, it will return an empty dataframe.
        """
        if not os.path.isfile(self.__src):
            return pd.DataFrame() 
        
        return pd.read_csv(self.__src, header=0)


    @classmethod
    def is_cache_available(cls) -> bool:
        """
        Checks whether the cache is available.
        Return:
            True if it is, False if it is not.
        """
        available: bool = True
        for filename in CACHE_PATH:
            available &= os.path.isfile(filename)

        return available
