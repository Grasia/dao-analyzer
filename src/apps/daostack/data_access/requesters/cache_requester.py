"""
   Descp: This class is used to load data from the datawarehouse.

   Created on: 16-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import pandas as pd
import os

from src.apps.daostack.data_access.requesters.irequester import IRequester
from src.logs import LOGS

CACHE_PATH: str = os.path.join('datawarehouse', 'daostack')
DAOS: str = os.path.join(CACHE_PATH, 'daos.csv')
PROPOSALS: str = os.path.join(CACHE_PATH, 'proposals.csv')
REP_HOLDERS: str = os.path.join(CACHE_PATH, 'reputation_holders.csv')
STAKES: str = os.path.join(CACHE_PATH, 'stakes.csv')
VOTES: str = os.path.join(CACHE_PATH, 'votes.csv')


class CacheRequester(IRequester):
    def request(self, *args) -> pd.DataFrame:
        """
        Requests data from datawarehouse.
        Arguments:
            * args: Takes its first argument and use it as path to load data.
        Return:
            a pandas dataframe with all the data loaded. If the path does not 
            exist, it will return an empty dataframe.
        """
        if len(args) < 1:
            raise AttributeError(LOGS['no_attr_cache_req'])

        path: str = args[0]
        if not os.path.isfile(path):
            return pd.DataFrame() 
        
        return pd.read_csv(path, header=0)
