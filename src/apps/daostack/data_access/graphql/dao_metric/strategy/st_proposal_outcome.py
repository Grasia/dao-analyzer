"""
   Descp: Strategy pattern for proposal's boost outcomes in a timeline 

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict, Tuple, Any
import pandas as pd

from src.apps.daostack.data_access.graphql.dao_metric.strategy.\
        strategy_metric_interface import StrategyInterface

from src.api.graphql.query import Query
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.serie import Serie
import src.apps.daostack.data_access.utils.pandas_utils as pd_utl


METRIC_TYPE_BOOST_OUTCOME: int = 0
METRIC_TYPE_BOOST_SUCCESS_RATIO: int = 1
METRIC_TYPE_TOTAL_SUCCESS_RATIO: int = 2


class StProposalOutcome(StrategyInterface):
    __DF_DATE = 'closedAt'
    __DF_PASS = 'hasPassed'
    __DF_BOOST = 'isBoosted'
    __DF_COUNT = 'count'
    __DF_COLS1 = [__DF_DATE, __DF_PASS, __DF_BOOST]
    __DF_COLS2 = [__DF_DATE, __DF_PASS, __DF_BOOST, __DF_COUNT]


    def __init__(self, m_type: int):
        self.__m_type = m_type


    def get_empty_df(self) -> pd.DataFrame:
        return pd_utl.get_empty_data_frame(self.__DF_COLS1)


    def __get_boost_from_dataframe(self, df: pd.DataFrame, boosted: bool)\
    -> Tuple[List[int]]:

        s_pass: List[int] = list()
        s_not_pass: List[int] = list()

        for _, row in df.iterrows():
            if row[self.__DF_BOOST] == boosted:
                if row[self.__DF_PASS]:
                    s_pass.append(row[self.__DF_COUNT])
                else:
                    s_not_pass.append(row[self.__DF_COUNT])

        return (s_not_pass, s_pass)


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        df = pd_utl.count_cols_repetitions(df=df, 
            cols=self.__DF_COLS1, new_col=self.__DF_COUNT)

        # generates a time serie
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)

        # joinning all the data in a unique dataframe and fill with all combinations
        for p in [True, False]:
            for b in [True, False]:
                dff = pd_utl.get_df_from_lists([idx, p, b, 0], self.__DF_COLS2)

                dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)
                df = df.append(dff, ignore_index=True)

        df.drop_duplicates(subset=self.__DF_COLS1,
        keep="first", inplace=True)
        df.sort_values(self.__DF_DATE, inplace=True, ignore_index=True)

        return self.generate_metric(df)


    def generate_metric(self, df: pd.DataFrame) -> Any:
        metric = StackedSerie()

        if self.__m_type == METRIC_TYPE_BOOST_OUTCOME:
            metric = self.get_boost_outcome(df)
        elif self.__m_type == METRIC_TYPE_BOOST_SUCCESS_RATIO:
            pass
        elif self.__m_type == METRIC_TYPE_TOTAL_SUCCESS_RATIO:
            pass

        return metric


    def get_boost_outcome(self, df: pd.DataFrame) -> StackedSerie:
        serie: Serie = Serie(x = df.drop_duplicates(subset=self.__DF_DATE,
            keep="first")[self.__DF_DATE].tolist())

        n_p1, p1 = self.__get_boost_from_dataframe(df, False)
        n_p2, p2 = self.__get_boost_from_dataframe(df, True)

        return StackedSerie(serie=serie, y_stack=[p1, p2, n_p2, n_p1])


    def get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
        return Query(
            header='proposals',
            body=['executedAt', 'executionState', 'winningOutcome'],
            filters={
                'where': f'{{dao: \"{o_id}\", executedAt_not: null}}',
                'first': f'{n_first}',
                'skip': f'{n_skip}',
            })


    def fetch_result(self, result: Dict) -> List:
        return result['proposals']

    
    def dict_to_df(self, data: List) -> pd.DataFrame:
        df: pd.DataFrame = self.get_empty_df()
        boost: List[str] = ['BoostedTimeOut', 'BoostedBarCrossed']

        for di in data:
            x: int = int(di['executedAt'])
            y: bool = True if di['winningOutcome'] == 'Pass' else False
            z: bool = True if any(x == di['executionState'] for x in boost)\
                else False

            df = pd_utl.append_rows(df, [x, y, z])

        return df
