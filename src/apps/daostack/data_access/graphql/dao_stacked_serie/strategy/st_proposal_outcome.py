"""
   Descp: Strategy pattern for proposal's type outcomes in a timeline 

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict, Tuple
import pandas as pd
from pandas.tseries.offsets import DateOffset
from datetime import datetime

from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
        strategy_metric_interface import StrategyInterface

from src.api.graphql.query import Query
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.serie import Serie


class StProposalOutcome(StrategyInterface):
    def get_empty_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=['closedAt', 'hasPassed', 'isBoosted'])


    def __get_boost_from_dataframe(self, df: pd.DataFrame, boosted: bool)\
        -> Tuple[List[int]]:

        s_pass: List[int] = list()
        s_not_pass: List[int] = list()

        for _, row in df.iterrows():
            if row['isBoosted'] == boosted:
                if row['hasPassed']:
                    s_pass.append(row['count'])
                else:
                    s_not_pass.append(row['count'])

        return (s_not_pass, s_pass)


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if df.shape[0] == 0:
            return StackedSerie()

        # takes just the month
        df['closedAt'] = pd.to_datetime(df['closedAt'], unit='s').dt.to_period('M')

        # groupby columns and count repetitions as a new column.
        df = df.groupby(['closedAt', 'hasPassed', 'isBoosted']).size().reset_index(name='count')
        df['closedAt'] = df['closedAt'].dt.to_timestamp()
        
        # generates a time serie
        today = datetime.now()
        today = datetime(today.year, today.month, 1)
        start = df['closedAt'].min() if len(df['closedAt']) > 0 else today 
        end = today
        idx = pd.date_range(start=start, end=end, freq=DateOffset(months=1))

        # joinning all the data in a unique dataframe and fill with all combinations
        for p in [True, False]:
            for b in [True, False]:
                dff = pd.DataFrame({
                    'closedAt': idx,
                    'hasPassed': p,
                    'isBoosted': b,
                    'count': 0})
                df = df.append(dff, ignore_index=True)

        df.drop_duplicates(subset=['closedAt', 'hasPassed', 'isBoosted'],
        keep="first", inplace=True)
        df.sort_values('closedAt', inplace=True, ignore_index=True)

        # generate metric output
        serie: Serie = Serie(x = df.drop_duplicates(subset='closedAt',
            keep="first")['closedAt'].tolist())

        n_p1, p1 = self.__get_boost_from_dataframe(df, False)
        n_p2, p2 = self.__get_boost_from_dataframe(df, True)

        return StackedSerie(serie=serie, y_stack=[p1, p2, n_p2, n_p1])


    def get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
        return Query(
                    header = 'dao',
                    body = Query(
                                header = 'proposals',
                                body = ['closingAt', 'executionState',
                                'winningOutcome'],
                                filters = {
                                    'first': f'{n_first}',
                                    'skip': f'{n_skip}',
                                },
                            ),
                    filters = {
                        'id': f'\"{o_id}\"',
                    })


    def fetch_result(self, result: Dict) -> List:
        return result['dao']['proposals']

    
    def dict_to_df(self, data: List) -> pd.DataFrame:
        df: pd.DataFrame = self.get_empty_df()
        boost: List[str] = ['BoostedTimeOut', 'BoostedBarCrossed']

        for di in data:
            x: int = None if di['closingAt'] == 'null' else int(di['closingAt'])
            y: bool = True if di['winningOutcome'] == 'Pass' else False
            z: bool = True if any(x == di['executionState'] for x in boost)\
                else False

            # just append closed proposals
            if x:
                serie: pd.Series = pd.Series([x, y, z], index=df.columns)
                df = df.append(serie, ignore_index=True)

        return df
