"""
   Descp: This is a dao (data access object) of stacked series.
    It's used to calculate proposal's type metric.
    It's used in order to warp the transformation among
    API's responses and the App's transfer.  

   Created on: 4-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict, Tuple
from pandas.tseries.offsets import DateOffset
from datetime import datetime
import pandas as pd

from src.app import DEBUG
from src.logs import LOGS
from src.apps.daostack.business.transfers.serie import Serie
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.api.graphql.query import Query
from src.api.graphql.query_builder import QueryBuilder
from src.apps.daostack.data_access.graphql.dao_stacked_serie.\
    dao_stacked_serie_interface import DaoStackedSerieInterface


class DaoProposalTypeMetric(DaoStackedSerieInterface):
    def __init__(self, ids: List[str], requester):
        self.__ids = ids
        self.__requester = requester


    def __dict_to_df(self, columns: List[str], data: List) -> pd.DataFrame:
        """
        Takes data and transforms it in a data frame which is returned.
        """
        df: pd.DataFrame = pd.DataFrame(columns = columns)
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


    def __get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
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


    def __request(self, o_id: str, columns: List[str]) -> pd.DataFrame:
        """
        Requests data and returns a pandas dataframe with columns distribution.
        Params:
            * o_id = An organization id
            * columns = Columns name for returned dataframe structure
        Return:
            * A pandas dataframe
        """
        chunk: int = 0
        result: Dict[str, List] = dict()
        df: pd.DataFrame = pd.DataFrame(columns = columns)
        condition: bool = True

        while condition:
            e_chunk = self.__requester.get_elems_per_chunk(chunk)
            query: Query = self.__get_query(n_first=e_chunk, n_skip=df.shape[0], 
                o_id=o_id)
            q_builder: QueryBuilder = QueryBuilder([query])

            result = self.__requester.request(q_builder.build())
            result = result['dao']['proposals']

            dff: pd.DataFrame = self.__dict_to_df(columns=columns, data=result)
            df = df.append(dff, ignore_index=True)

            condition = len(result) == e_chunk
            chunk += 1

        return df


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


    def __process_data(self, df: pd.DataFrame) -> StackedSerie:
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


    def get_stacked_serie(self) -> StackedSerie:
        start: datetime = datetime.now()
        df: pd.DataFrame = pd.DataFrame(columns=['closedAt', 'hasPassed',
        'isBoosted'])

        for o_id in self.__ids:
            dff: pd.DataFrame = self.__requester.__request(o_id=o_id, columns=df.columns)
            df = df.append(dff, ignore_index=True)

        if DEBUG:
            duration: int = (datetime.now() - start).total_seconds()
            print(LOGS['daos_requested'].format(len(self.__ids), duration))

        return self.__process_data(df)
