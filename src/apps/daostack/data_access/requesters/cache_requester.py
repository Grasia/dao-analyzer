"""
   Descp: This class is used to load data from the datawarehouse.

   Created on: 16-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import pandas as pd
import os

from src.apps.daostack.data_access.requesters.irequester import IRequester



class CacheRequester(IRequester):
    def request(self, *args) -> pd.DataFrame:
        """
        Requests data from datawarehouse.
        Arguments:
            * args: Takes its first argument and use it as path to load data.
        Return:
            a pandas dataframe with all the data loaded. If the path does not 
            exist, it will return an empty data frame.
        """
        if len(args) < 1:
            raise AttributeError('\'args\' has to be filled with a cache path.\n')

        path: str = args[0]
        if not os.path.isfile(path):
            return pd.DataFrame()
        
        return pd.read_csv(path, header=0)
