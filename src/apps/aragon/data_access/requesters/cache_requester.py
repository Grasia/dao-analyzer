"""
   Descp: This class is used to load data from the datawarehouse.

   Created on: 16-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import pandas as pd
import os
from typing import List

from src.apps.common.data_access.requesters.irequester import IRequester

CACHE_PATH: str = os.path.join('datawarehouse', 'aragon')
APPS: str = os.path.join(CACHE_PATH, 'apps.csv')
CASTS: str = os.path.join(CACHE_PATH, 'casts.csv')
MINI_ME_TOKENS: str = os.path.join(CACHE_PATH, 'miniMeTokens.csv')
ORGANIZATIONS: str = os.path.join(CACHE_PATH, 'organizations.csv')
REPOS: str = os.path.join(CACHE_PATH, 'repos.csv')
TOKEN_HOLDERS: str = os.path.join(CACHE_PATH, 'tokenHolders.csv')
TRANSACTIONS: str = os.path.join(CACHE_PATH, 'transactions.csv')
VOTES: str = os.path.join(CACHE_PATH, 'votes.csv')
ALL_FILES: List[str] = [
    APPS,
    CASTS,
    MINI_ME_TOKENS,
    ORGANIZATIONS,
    REPOS,
    TOKEN_HOLDERS,
    TRANSACTIONS,
    VOTES
]


class CacheRequester(IRequester):
    def __init__(self, srcs: List[str]):
        self.__srcs = srcs


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
            if os.path.isfile(src):
                df = pd.concat([df, pd.read_csv(src, header=0)], axis=0, ignore_index=True)
        
        return df


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
