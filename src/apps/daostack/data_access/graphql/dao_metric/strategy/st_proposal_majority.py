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
    __DF_MAJORITY_PER = 'majorityPer'
    __DF_IS_ABSOLUTE = 'isAbsolute'
    __DF_COLS = [__DF_DATE, __DF_PASS, __DF_MAJORITY_PER, __DF_IS_ABSOLUTE]


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
        dff = pd_utl.get_df_from_lists([idx, None, None, None], self.__DF_COLS)
        dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)

        df = df.append(dff, ignore_index=True)
        #df.drop_duplicates(subset=self.__DF_DATE, keep="first", inplace=True)
        df.sort_values(self.__DF_DATE, inplace=True, ignore_index=True)

        return self.generate_metric(df)


    def generate_metric(self, df: pd.DataFrame) -> NStackedSerie:
        abs_passes, rel_passes = self.__get_sserie_outcome(df=df, has_pass=True)
        abs_fails, rel_fails = self.__get_sserie_outcome(df=df, has_pass=False)

        return NStackedSerie(sseries=[abs_passes, rel_passes, rel_fails, abs_fails])


    def __get_sserie_outcome(self, df: pd.DataFrame, has_pass: bool)\
    -> (StackedSerie, StackedSerie):

        # invert has_pass 'cause the df col has True, False and None values.
        dff: pd.DataFrame = pd_utl.filter_by_col_value(df, self.__DF_PASS, 
            (not has_pass), [pd_utl.NEQ])
        # absolute
        d3f: pd.DataFrame = pd_utl.filter_by_col_value(dff, self.__DF_IS_ABSOLUTE, 
            False, [pd_utl.NEQ])
        absolute: StackedSerie = self.__get_sserie_from_df(d3f)
        # relative
        d3f: pd.DataFrame = pd_utl.filter_by_col_value(dff, self.__DF_IS_ABSOLUTE, 
            True, [pd_utl.NEQ])
        relative: StackedSerie = self.__get_sserie_from_df(d3f)

        return (absolute, relative)


    def __get_sserie_from_df(self, df: pd.DataFrame) -> StackedSerie:
        serie: Serie = Serie(x=df[self.__DF_DATE].tolist())
        return StackedSerie(serie=serie, y_stack=[df[
            self.__DF_MAJORITY_PER].tolist()])


    def get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
        return Query(
            header='proposals',
            body=['executedAt', 'winningOutcome', 'totalRepWhenExecuted', 
                'votesFor', 'votesAgainst', 'boostedAt' ,
                'genesisProtocolParams{queuedVoteRequiredPercentage}'],
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
            # winning outcome means more votes for than votes against
            outcome: bool = True if di['winningOutcome'] == 'Pass' else False
            boost: bool = True if di['boostedAt'] else False

            percentage: int = (int(di['votesFor']) / total) if outcome \
                else (int(di['votesAgainst']) / total)
            percentage = int(round(percentage * 100))

            is_absolute: bool  = True if \
                int(di['genesisProtocolParams']['queuedVoteRequiredPercentage'])\
                <= percentage else False

            has_passed: bool = False
            if outcome:
                has_passed = boost or is_absolute

            df = pd_utl.append_rows(df, [date, has_passed, percentage, is_absolute])

        return df
