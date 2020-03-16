"""
   Descp: Strategy pattern for create simple metrics based on time series.

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
import pandas as pd

from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
        strategy_metric_interface import StrategyInterface

from src.api.graphql.query import Query
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.serie import Serie
import src.apps.daostack.data_access.utils.pandas_utils as pd_utl


METRIC_TYPE_NEW_USERS: int = 0
METRIC_TYPE_NEW_PROPOSAL: int = 1


class StTimeSerie(StrategyInterface):
    __DF_DATE = 'date'
    __DF_COUNT = 'count'
    __DF_COLS = [__DF_DATE, __DF_COUNT]


    def __init__(self, m_type: int):
        self.__m_type = self.__get_type(m_type)


    def __get_type(self, m_type: int) -> str:
        m_key: str = ''
        if m_type == METRIC_TYPE_NEW_USERS:
            m_key = 'reputationHolders'
        elif m_type == METRIC_TYPE_NEW_PROPOSAL:
            m_key = 'proposals'

        return m_key


    def get_empty_df(self) -> pd.DataFrame:
        return pd_utl.get_empty_data_frame([self.__DF_DATE])


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        
        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        df = pd_utl.count_cols_repetitions(df, [self.__DF_DATE], self.__DF_COUNT)
        
        # generates a time series
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)

        dff = pd_utl.get_df_from_lists([idx, 0], self.__DF_COLS)
        dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)

        # joinning all the data in a unique dataframe
        df = df.append(dff, ignore_index=True)
        df.drop_duplicates(subset=self.__DF_DATE, keep="first", inplace=True)
        df.sort_values(self.__DF_DATE, inplace=True)
        
        serie: Serie = Serie(x=df[self.__DF_DATE].tolist())
        metric: StackedSerie = StackedSerie(
            serie = serie, 
            y_stack = [df[self.__DF_COUNT].tolist()])

        return metric


    def get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
        return Query(
            header=self.__m_type,
            body=['createdAt'],
            filters={
                'where': f'{{dao: \"{o_id}\"}}',
                'first': f'{n_first}',
                'skip': f'{n_skip}',
            })


    def fetch_result(self, result: Dict) -> List:
        return result[self.__m_type]

    
    def dict_to_df(self, data: List) -> pd.DataFrame:
        df: pd.DataFrame = self.get_empty_df()

        for di in data:
            df = pd_utl.append_rows(df, [di['createdAt']])

        return df
