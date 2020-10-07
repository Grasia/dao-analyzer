"""
   Descp: Strategy pattern to create a metric of new members.

   Created on: 5-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd

from src.apps.common.data_access.daos.metric.imetric_strategy \
    import IMetricStrategy
from src.apps.common.business.transfers.stacked_serie import StackedSerie
from src.apps.common.business.transfers.serie import Serie
import src.apps.common.data_access.pandas_utils as pd_utl


class StNewMembers(IMetricStrategy):
    __DF_DATE = 'createdAt'
    __DF_COUNT = 'count'
    __DF_EXISTS = 'exists'
    __DF_COLS = [__DF_DATE, __DF_COUNT]


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
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
        df = df.append(dff, ignore_index=True)
        df.drop_duplicates(subset=self.__DF_DATE, keep="first", inplace=True)
        df.sort_values(self.__DF_DATE, inplace=True)
        
        serie: Serie = Serie(x=df[self.__DF_DATE].tolist())
        metric: StackedSerie = StackedSerie(
            serie = serie, 
            y_stack = [df[self.__DF_COUNT].tolist()])

        return metric
