"""
   Descp: Strategy pattern for calculate differents voters and stakers by month.

   Created on: 17-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
import pandas as pd

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl


VOTERS = 0
STAKERS = 1


class StDifferentVS(IMetricStrategy):
    __DF_DATE = 'createdAt'
    __DF_VOTER = 'voter'
    __DF_STAKER = 'staker'
    __DF_COUNT = 'count'


    def __init__(self, m_type: int):
        self.__DF_COLS: List[str] = self.__get_df_columns(m_type)


    def __get_df_columns(self, m_type: int) -> List[str]:
        cols: List[str] = [self.__DF_DATE]
        if m_type == VOTERS:
            cols.append(self.__DF_VOTER)
        elif m_type == STAKERS:
            cols.append(self.__DF_STAKER)
        else:
            raise Exception(f'{m_type} type not allowed')

        return cols


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        dff.loc[:, self.__DF_COLS] = dff[self.__DF_COLS]
        return dff


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        df = self.clean_df(df=df)

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
        df = pd.concat([df, dff], ignore_index=True)
        df = df.drop_duplicates(subset=self.__DF_DATE, keep="first")
        df = df.sort_values(self.__DF_DATE)

        serie: Serie = Serie(x=df[self.__DF_DATE].tolist())
        metric: StackedSerie = StackedSerie(
            serie = serie, 
            y_stack = [df[self.__DF_COUNT].tolist()])

        return metric
