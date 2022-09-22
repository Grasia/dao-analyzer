"""
   Descp: Strategy pattern to create a metric of new additions.

   Created on: 5-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from typing import List

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl


class StNewAdditions(IMetricStrategy):
    MEMBERS = 0
    OUTGOING_MEMBERS = 1
    PROPOSALS = 2
    VOTES = 3
    __TYPES: List[int] = [MEMBERS, OUTGOING_MEMBERS, PROPOSALS, VOTES]

    __DF_DATE = 'createdAt'
    __DF_COUNT = 'count'
    __DF_EXISTS = 'exists'
    __DF_COLS = [__DF_DATE, __DF_COUNT]


    def __init__(self, typ: int) -> None:
        self.__typ: int = self.__get_type(typ)


    def __get_type(self, typ: int) -> int:
        """
        Checks if typ exists, if not return by default the first type
        """
        return typ if typ in self.__TYPES else self.__TYPES[0]


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df

        if self.__typ is self.MEMBERS:
            dff.loc[:, :] = dff[dff[self.__DF_EXISTS]]

        dff.loc[:, [self.__DF_DATE]] = dff[[self.__DF_DATE]]
        return dff


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        
        df = self.clean_df(df=df)

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        df = pd_utl.count_cols_repetitions(df, [self.__DF_DATE], self.__DF_COUNT)
        
        # generates a time series
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)

        dff = pd_utl.get_df_from_lists([idx, 0], self.__DF_COLS)
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
