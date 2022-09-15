"""
   Descp: Strategy pattern to calculate active users, the ones who performs
   at least one action (create a proposal, vote or stake) in a given month. 

   Created on: 24-aug-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
import pandas as pd

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl


class StActiveUsers(IMetricStrategy):
    __DF_DATE = 'createdAt'
    __DF_PROPOSER = 'proposer'
    __DF_VOTER = 'voter'
    __DF_STAKER = 'staker'
    __DF_USER = 'user'
    __DF_COUNT = 'activeUsers'
    __DF_COLS = [__DF_DATE, __DF_USER]


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        actioners = set([self.__DF_PROPOSER, self.__DF_VOTER, self.__DF_STAKER])
        actioners = list(actioners.intersection(set(df.columns)))
        used_cols: List[str] = actioners + [self.__DF_DATE]
        dff = dff[used_cols]
        return dff


    def __get_user_action(self, df: pd.DataFrame, actioner: str) -> pd.DataFrame:
        if actioner not in df.columns:
            return pd.DataFrame()

        columns: List[str] = [self.__DF_DATE, actioner]
        dff = df[columns]
        dff = dff.dropna(subset=[actioner])
        return dff.rename(columns={actioner: self.__DF_USER})


    def __prepare_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Changes the columns proposer, voter and staker into an unique column
        named user.
        """
        return pd.concat([
            self.__get_user_action(df, self.__DF_PROPOSER),
            self.__get_user_action(df, self.__DF_VOTER),
            self.__get_user_action(df, self.__DF_STAKER)
        ], ignore_index=True)


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        df = self.clean_df(df=df)
        df = self.__prepare_df(df=df)

        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        # join dates-ids
        df = pd_utl.count_cols_repetitions(df, self.__DF_COLS, self.__DF_COUNT)
        # different users by month
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
