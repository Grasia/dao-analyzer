"""
   Descp: Strategy pattern for total votes metric.

   Created on: 16-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import pandas as pd
from typing import List, Dict

from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
        strategy_metric_interface import StrategyInterface
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.api.graphql.query import Query
import src.apps.daostack.data_access.utils.pandas_utils as pd_utl


class StTotalVotes(StrategyInterface):
    __DF_DATE = 'date'
    __DF_VOTES = 'votes'
    __DF_TOTAL = 'total'
    __DF_COLS = [__DF_DATE, __DF_VOTES]


    def get_empty_df(self) -> pd.DataFrame:
        return pd_utl.get_empty_data_frame(self.__DF_COLS)


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        df = pd_utl.sum_cols_repetitions(df, self.__DF_DATE, self.__DF_TOTAL)

        print(df)

        return StackedSerie()

    
    def get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
        return Query(
            header='proposals',
            body=['votesFor', 'votesAgainst', 'executedAt'],
            filters={
                'where': f'{{dao: \"{o_id}\"}}',
                'first': f'{n_first}',
                'skip': f'{n_skip}',
            })

    
    def fetch_result(self, result: Dict) -> List:
        return result['proposals']

    
    def dict_to_df(self, data: List) -> pd.DataFrame:
        df: pd.DataFrame = self.get_empty_df()

        for di in data:
            date: int = int(di['executedAt'])
            votes: int = int(di['votesFor']) + int(di['votesAgainst'])
            df = pd_utl.append_rows(df, [date, votes])

        return df
