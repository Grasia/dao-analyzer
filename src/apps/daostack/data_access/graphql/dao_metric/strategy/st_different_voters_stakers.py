"""
   Descp: Strategy pattern for calculate differents voters and stakers by month.

   Created on: 17-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
import pandas as pd

from src.apps.daostack.data_access.graphql.dao_metric.strategy.\
        strategy_metric_interface import StrategyInterface

from src.api.graphql.query import Query
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.serie import Serie
import src.apps.daostack.data_access.utils.pandas_utils as pd_utl


VOTERS = 0
STAKERS = 1


class StDifferentVS(StrategyInterface):
    __DF_DATE = 'createdAt'
    __DF_USER_ID = 'userId'
    __DF_COUNT = 'count'
    __DF_COLS = [__DF_DATE, __DF_USER_ID]
    __SCHEMA_VOTER = {
        'schema': 'proposalVotes',
        'attrs': ['createdAt', 'voter'],
    }
    __SCHEMA_STAKER = {
        'schema': 'proposalStakes',
        'attrs': ['createdAt', 'staker'],
    }
    __SCHEMAS = [__SCHEMA_VOTER, __SCHEMA_STAKER]


    def __init__(self, m_type: int):
        self.__m_index: int = self.__get_index(m_type)


    def __get_index(self, m_type: int) -> int:
        index: int = -1
        if m_type == VOTERS:
            index = 0
        elif m_type == STAKERS:
            index = 1
        else:
            raise Exception(f'{m_type} type not allowed')

        return index


    def get_empty_df(self) -> pd.DataFrame:
        return pd_utl.get_empty_data_frame(self.__DF_COLS)


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        # join dates-ids
        df = pd_utl.count_cols_repetitions(df, self.__DF_COLS, self.__DF_COUNT)
        # different voters by month
        df = pd_utl.count_cols_repetitions(df, [self.__DF_DATE], self.__DF_COUNT)

        # generates a time series
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)
        dff = pd_utl.get_df_from_lists([idx, 0], [self.__DF_DATE, self.__DF_COUNT])
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
            header=self.__SCHEMAS[self.__m_index]['schema'],
            body=self.__SCHEMAS[self.__m_index]['attrs'],
            filters={
                'where': f'{{dao: \"{o_id}\"}}',
                'first': f'{n_first}',
                'skip': f'{n_skip}',
            })


    def fetch_result(self, result: Dict) -> List:
        return result[self.__SCHEMAS[self.__m_index]['schema']]

    
    def dict_to_df(self, data: List) -> pd.DataFrame:
        df: pd.DataFrame = self.get_empty_df()
        attrs: List[str]

        for di in data:
            attrs = list()
            for k in self.__SCHEMAS[self.__m_index]['attrs']:
                attrs.append(di[k])

            df = pd_utl.append_rows(df, attrs)

        return df
