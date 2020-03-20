"""
   Descp: Strategy pattern for proposal's majority outcome

   Created on: 20-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
import pandas as pd

from src.apps.daostack.data_access.graphql.dao_metric.strategy.\
        strategy_metric_interface import StrategyInterface

from src.api.graphql.query import Query
from src.apps.daostack.business.transfers.n_stacked_serie import NStackedSerie
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.serie import Serie
import src.apps.daostack.data_access.utils.pandas_utils as pd_utl


class StProposalMajority(StrategyInterface):
    __DF_DATE = 'closedAt'
    __DF_PASS = 'outcome'
    __DF_MAJORITY = 'majorityPer'
    __DF_COLS = [__DF_DATE, __DF_PASS, __DF_MAJORITY]


    def get_empty_df(self) -> pd.DataFrame:
        return pd_utl.get_empty_data_frame(self.__DF_COLS)


    def process_data(self, df: pd.DataFrame) -> NStackedSerie:
        if pd_utl.is_an_empty_df(df):
            return NStackedSerie()

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        # generates a time serie
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)

        # joinning all the data in a unique dataframe and fill with NA values
        dff = pd_utl.get_df_from_lists([idx, None, None], self.__DF_COLS)
        dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)

        df = df.append(dff, ignore_index=True)
        #df.drop_duplicates(subset=self.__DF_DATE, keep="first", inplace=True)
        df.sort_values(self.__DF_DATE, inplace=True, ignore_index=True)

        # generate metric output
        dff: pd.DataFrame = pd_utl.filter_by_col_value(df, self.__DF_PASS, 
            False, [pd_utl.NEQ])
        serie: Serie = Serie(x=dff[self.__DF_DATE].tolist())
        passes: StackedSerie = StackedSerie(serie=serie, 
            y_stack=[dff[self.__DF_MAJORITY].tolist()])

        dff: pd.DataFrame = pd_utl.filter_by_col_value(df, self.__DF_PASS, 
            True, [pd_utl.NEQ])
        serie: Serie = Serie(x=dff[self.__DF_DATE].tolist())
        fails: StackedSerie = StackedSerie(serie=serie, 
            y_stack=[dff[self.__DF_MAJORITY].tolist()])

        return NStackedSerie(sseries=[passes, fails])


    def get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
        return Query(
            header='proposals',
            body=['executedAt', 'winningOutcome', 'totalRepWhenExecuted', 
                'votesFor', 'votesAgainst'],
            filters={
                'where': f'{{dao: \"{o_id}\", executedAt_not: null}}',
                'first': f'{n_first}',
                'skip': f'{n_skip}',
            })


    def fetch_result(self, result: Dict) -> List:
        return result['proposals']

    
    def dict_to_df(self, data: List) -> pd.DataFrame:
        df: pd.DataFrame = self.get_empty_df()

        for di in data:
            total: int = int(di['totalRepWhenExecuted'])
            if total == 0:
                continue

            date: int = int(di['executedAt'])
            outcome: bool = True if di['winningOutcome'] == 'Pass' else False

            percentage: int = int(di['votesFor']) / total if outcome \
                else int(di['votesAgainst']) / total
            percentage = int(round(percentage * 100))

            df = pd_utl.append_rows(df, [date, outcome, percentage])

        return df
