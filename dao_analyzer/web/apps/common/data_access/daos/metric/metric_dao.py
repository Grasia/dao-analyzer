"""
   Descp: This is a dao (data access object) of metrics.
    It's used as interface to transform data from the datawarehouse
    and transfers like serie, stackedSerie, NStackedSerie.  

   Created on: 17-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
import pandas as pd

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.data_access.requesters.irequester import IRequester


class MetricDao():
    def __init__(self, ids: List[str], strategy: IMetricStrategy,
     requester: IRequester, address_key: str):
        self.__ids = ids
        self.__st = strategy
        self.__requester = requester
        self.__address_key = address_key


    def get_metric(self):
        df: pd.DataFrame = self.__requester.request()
        assert(not df.empty)
        
        # get only data from daos in ids
        df = df.loc[df[self.__address_key].isin(self.__ids)]
        
        # So process_data doesn't modify it
        df = df.copy()

        return self.__st.process_data(df)
