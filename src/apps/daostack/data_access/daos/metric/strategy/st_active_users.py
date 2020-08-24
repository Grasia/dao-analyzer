"""
   Descp: Strategy pattern to calculate active users, the ones who performs
   at least one action (create a proposal, vote or stake) in a given month. 

   Created on: 24-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
import pandas as pd

from src.apps.daostack.data_access.daos.metric.strategy.\
        strategy_metric_interface import StrategyInterface

from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.serie import Serie
import src.apps.daostack.data_access.utils.pandas_utils as pd_utl


class StActiveUsers(StrategyInterface):
    __DF_DATE = 'createdAt'
    __DF_PROPOSER = 'proposer'
    __DF_VOTER = 'voter'
    __DF_STAKER = 'staker'
    __DF_USER = 'user'
    __DF_COUNT = 'activeUsers'
    __DF_COLS = [__DF_DATE, __DF_USER]


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        used_cols = [self.__DF_DATE, self.__DF_PROPOSER, self.__DF_VOTER, self.__DF_STAKER]
        dff = dff[used_cols]
        return dff


    def __get_user_action(self, df: pd.DataFrame, actioner: str) -> pd.DataFrame:
        columns: List[str] = [self.__DF_DATE, actioner]
        dff = df[columns]
        dff = dff.dropna(subset=[actioner])
        return dff.rename(columns={actioner: self.__DF_USER})


    def __prepare_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Changes the columns proposer, voter and staker into an unique column
        named user.
        """
        dff: pd.DataFrame = self.__get_user_action(df=df, actioner=self.__DF_PROPOSER)
        dff = dff.append(self.__get_user_action(df=df, actioner=self.__DF_VOTER), ignore_index=True)
        dff = dff.append(self.__get_user_action(df=df, actioner=self.__DF_STAKER), ignore_index=True)
        return dff


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        df = self.clean_df(df=df)
        df = self.__prepare_df(df=df)

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
        df = df.append(dff, ignore_index=True)
        df.drop_duplicates(subset=self.__DF_DATE, keep="first", inplace=True)
        df.sort_values(self.__DF_DATE, inplace=True)

        serie: Serie = Serie(x=df[self.__DF_DATE].tolist())
        metric: StackedSerie = StackedSerie(
            serie = serie, 
            y_stack = [df[self.__DF_COUNT].tolist()])

        return metric
