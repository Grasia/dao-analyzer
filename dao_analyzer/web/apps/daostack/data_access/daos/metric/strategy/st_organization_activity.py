"""
    Descp: Strategy pattern to add the activity of each DAO per month.
           It'll add proposals created and votes and transactions.
    Created on: 27-apr-2022
    Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
import pandas as pd

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy.imetric_strategy import IMetricStrategy

from dao_analyzer.web.apps.common.business.transfers import Serie, StackedSerie
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl

class StOrganizationActivity(IMetricStrategy):
    __DF_DATE = 'createdAt'
    __DF_ID = 'dao'
    __DF_COUNT = 'count'
    __DF_COLS = [__DF_DATE, __DF_ID]


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
        # different users by month
        df = pd_utl.sum_cols_repetitions(df, [self.__DF_DATE], self.__DF_COUNT)

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
