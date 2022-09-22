"""
   Descp: Strategy pattern to create a proposal type metric.

   Created on: 9-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from typing import List, Tuple

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl


class StProposalType(IMetricStrategy):
    __GRANT_PROPOSAL = 0
    __NEW_MEMBER_PROPOSAL = 1
    __DONATION_PROPOSAL = 2
    __OTHER_PROPOSAL = 3

    __DF_DATE = 'createdAt'
    __DF_COUNT = 'count'
    __DF_TRIBUTE = 'tributeOffered'
    __DF_SHARES = 'sharesRequested'
    __DF_TYPE = 'type'
    __DF_COLS = [__DF_DATE, __DF_TYPE]


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        dff.loc[:, [self.__DF_DATE, self.__DF_SHARES, self.__DF_TRIBUTE]] = \
            dff[[self.__DF_DATE, self.__DF_SHARES, self.__DF_TRIBUTE]]
        return dff


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        df = self.clean_df(df=df)
        df = self.__transform_df(df=df)

        df = pd_utl.count_cols_repetitions(df, self.__DF_COLS, self.__DF_COUNT)
        
        # generates a time series
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)
        dff = pd_utl.get_df_from_lists([idx, 0], [self.__DF_DATE, self.__DF_COUNT])
        dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)

        serie: Serie = Serie(x=dff[self.__DF_DATE].tolist())
        grants: List = self.__get_proposals_type(self.__GRANT_PROPOSAL, df, dff)
        new_members: List = self.__get_proposals_type(self.__NEW_MEMBER_PROPOSAL, df, dff)
        donations: List = self.__get_proposals_type(self.__DONATION_PROPOSAL, df, dff)
        others: List = self.__get_proposals_type(self.__OTHER_PROPOSAL, df, dff)

        metric: StackedSerie = StackedSerie(
            serie = serie,
            y_stack = [others, donations, new_members, grants])

        return metric


    def __get_proposals_type(self, typ: int, df: pd.DataFrame, 
    dff: pd.DataFrame) -> List[int]:

        d3f: pd.DataFrame = pd_utl.filter_by_col_value(
            df=df, 
            col=self.__DF_TYPE, 
            value=typ,
            filters=[pd_utl.EQ])

        d3f = d3f.drop(columns=[self.__DF_TYPE])
        d3f = pd.concat([d3f, dff], ignore_index=True)
        d3f = d3f.drop_duplicates(subset=self.__DF_DATE, keep="first")
        d3f = d3f.sort_values(self.__DF_DATE)

        return d3f[self.__DF_COUNT].tolist()


    def __transform_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        payments: List[Tuple[int, int]] = \
            tuple(zip(dff[self.__DF_SHARES].tolist(), dff[self.__DF_TRIBUTE].tolist()))
        
        types: List[int] = list(map(self.__get_type, payments))
        dff[self.__DF_TYPE] = types

        # takes just the month
        dff = pd_utl.unix_to_date(dff, self.__DF_DATE)
        dff = pd_utl.transform_to_monthly_date(dff, self.__DF_DATE)

        return dff


    def __get_type(self, tup: Tuple[int, int]) -> int:
        share, tribute = tup
        typ: int = self.__OTHER_PROPOSAL

        if int(share) > 0 and int(tribute) == 0:
            typ = self.__GRANT_PROPOSAL
        elif int(share) > 0 and int(tribute) > 0:
            typ = self.__NEW_MEMBER_PROPOSAL
        elif int(share) == 0 and int(tribute) > 0:
            typ = self.__DONATION_PROPOSAL

        return typ
