"""
   Descp: Strategy pattern to create a votation outcome metric.

   Created on: 21-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from typing import List

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl


class StVoteOutcome(IMetricStrategy):
    __DECIMALS = 10000000000000000
    __DF_DATE = 'startDate'
    __DF_EXECUTED = 'executed'
    __DF_YEA = 'yea'
    __DF_NAY = 'nay'
    __DF_SUPPORT = 'supportRequiredPct'
    __DF_VOTING = 'votingPower'
    __DF_QUORUM = 'minAcceptQuorum'
    __DF_PASS = 'didPass'
    __DF_COUNT = 'count'
    __DF_COLS = [__DF_DATE, __DF_YEA, __DF_NAY, __DF_SUPPORT, __DF_VOTING, __DF_QUORUM]


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        # just take closed proposals
        # dff = pd_utl.filter_by_col_value(
        #     df=dff, 
        #     col=self.__DF_EXECUTED, 
        #     value=True,
        #     filters=[pd_utl.EQ])

        dff.loc[:, self.__DF_COLS] = dff[self.__DF_COLS]
        return dff


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        df = self.clean_df(df=df)
        df = self.__calculate_outcome(df=df)

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        df = pd_utl.count_cols_repetitions(df, [self.__DF_DATE, self.__DF_PASS], self.__DF_COUNT)
        
        # generates a time series
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)
        dff = pd_utl.get_df_from_lists([idx, 0], [self.__DF_DATE, self.__DF_COUNT])
        dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)

        serie: Serie = Serie(x=dff[self.__DF_DATE].tolist())
        passes: List = self.__get_outcome(True, df, dff)
        rejections: List = self.__get_outcome(False, df, dff)

        metric: StackedSerie = StackedSerie(
            serie = serie,
            y_stack = [rejections, passes])

        return metric


    def __get_outcome(self, has_pass: bool, df: pd.DataFrame, 
    dff: pd.DataFrame) -> List[int]:

        d3f: pd.DataFrame = pd_utl.filter_by_col_value(
            df=df, 
            col=self.__DF_PASS, 
            value=has_pass,
            filters=[pd_utl.EQ])

        d3f = d3f.drop(columns=[self.__DF_PASS])
        d3f = pd.concat([d3f, dff], ignore_index=True)
        d3f = d3f.drop_duplicates(subset=self.__DF_DATE, keep="first")
        d3f = d3f.sort_values(self.__DF_DATE)

        return d3f[self.__DF_COUNT].tolist()


    def __calculate_outcome(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        outcome = ((positive voted tokens) / total voted tokens * 100) >= support required
                and
                ((positive voted tokens) / total tokens * 100) >= minimum accepted quorum
        """
        dff: pd.DataFrame = df

        has_pass: List[bool] = []
        yea: List[int] = [int(x) for x in dff[self.__DF_YEA].tolist()]
        nay: List[int] = [int(x) for x in dff[self.__DF_NAY].tolist()]
        total: List[int] = [int(x) for x in dff[self.__DF_VOTING].tolist()]
        l_support: List[int] = [int(x) for x in dff[self.__DF_SUPPORT].tolist()]
        l_quorum: List[int] = [int(x) for x in dff[self.__DF_QUORUM].tolist()]

        for i in range(len(dff)):
            support: int = self.__percentage(l_support[i])
            quorum: int = self.__percentage(l_quorum[i])

            positive_support: int = self.__ratio(yea[i], (yea[i] + nay[i])) * 100
            total_support: int = self.__ratio(yea[i], total[i]) * 100
            
            has_pass.append( (positive_support >= support) and (total_support >= quorum) )

        dff.loc[:, self.__DF_PASS] = has_pass
        dff.loc[:, [self.__DF_DATE, self.__DF_PASS]] = \
            dff[[self.__DF_DATE, self.__DF_PASS]]

        return dff


    def __percentage(self, value: int) -> int:
        """
        transform big int Aragon percentage into a normal percentage
        """
        return value / self.__DECIMALS


    def __ratio(self, num: int, divider: int) -> int:
        if divider == 0:
            return 0

        return num / divider
