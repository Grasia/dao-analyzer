"""
   Descp: Strategy pattern to create total reputation holders.

   Created on: 05-nov-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from typing import List

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie 
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl
import dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_time_serie \
    as new_reputation_holders


class StTotalRepHolders(IMetricStrategy):

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        
        new_holders: StackedSerie = new_reputation_holders\
            .StTimeSerie(m_type=new_reputation_holders.NEW_USERS).process_data(df)

        total: List[int] = self.__calculate_total(new_holders=new_holders)

        metric: StackedSerie = StackedSerie(
            serie = Serie(x=new_holders.get_serie()), 
            y_stack = [total])

        return metric


    def __calculate_total(self, new_holders: StackedSerie) -> List[int]:
        news: List[int] = new_holders.get_i_stack(0)
        total: List[int] = [news[0]]

        for i in range(1, len(news)):
            total.append(news[i] + total[i-1])

        return total
