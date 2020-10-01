"""
   Descp: Strategy pattern for calculate votes/stakes outcome.

   Created on: 30-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
import pandas as pd

from src.apps.daostack.data_access.daos.metric.strategy.\
        strategy_metric_interface import IMetricStrategy
from src.apps.common.business.transfers.stacked_serie import StackedSerie
from src.apps.common.business.transfers.serie import Serie
import src.apps.daostack.data_access.utils.pandas_utils as pd_utl


VOTES = 0
STAKES = 1


class StTotalVSOption(IMetricStrategy):
    __DF_DATE = 'createdAt'
    __DF_OUTCOME = 'outcome'
    __DF_IS_POSITIVE = 'isPositive'
    __DF_COUNT = 'count'
    __DF_COLS = [__DF_DATE, __DF_IS_POSITIVE]
    __DF_INI_COLS = [__DF_DATE, __DF_OUTCOME]


    def __init__(self, m_type: int):
        self.__type: int = m_type


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        dff.loc[:, self.__DF_INI_COLS] = dff[self.__DF_INI_COLS]
        return dff


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        df = self.clean_df(df=df)
        df = self.__transform_df(df=df)

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        # join by dates
        df = pd_utl.count_cols_repetitions(df, self.__DF_COLS, self.__DF_COUNT)

        # generates a time serie
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)
        dff = pd_utl.get_df_from_lists([idx, 0], [self.__DF_DATE, self.__DF_COUNT])
        dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)

        serie: Serie = Serie(x=dff[self.__DF_DATE].tolist())
        positives: List = self.__get_outcome(True, df, dff)
        negatives: List = self.__get_outcome(False, df, dff)

        metric: StackedSerie = StackedSerie(
            serie = serie, 
            y_stack = [negatives, positives])

        return metric


    def __get_outcome(self, is_positive: bool, df: pd.DataFrame, dff: pd.DataFrame) -> List:
        d3f: pd.DataFrame = pd_utl.filter_by_col_value(
            df=df, 
            col=self.__DF_IS_POSITIVE, 
            value=is_positive,
            filters=[pd_utl.EQ])

        d3f = d3f.drop(columns=[self.__DF_IS_POSITIVE])
        d3f = d3f.append(dff, ignore_index=True)
        d3f.drop_duplicates(subset=self.__DF_DATE, keep="first", inplace=True)
        d3f.sort_values(self.__DF_DATE, inplace=True)

        return d3f[self.__DF_COUNT].tolist()

    
    def __transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = pd_utl.get_empty_data_frame(self.__DF_COLS)

        for _, row in df.iterrows():
            date: int = int(row[self.__DF_DATE])
            is_positive: bool = True if row[self.__DF_OUTCOME] == 'Pass' else False

            dff = pd_utl.append_rows(dff, [date, is_positive])

        return dff
