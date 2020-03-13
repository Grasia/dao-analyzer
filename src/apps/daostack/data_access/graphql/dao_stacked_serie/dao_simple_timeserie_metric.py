"""
   Descp: This is a dao (data access object) of stacked series.
    It can process simple time series.  

   Created on: 26-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
import pandas as pd
from pandas.tseries.offsets import DateOffset
from datetime import datetime

from src.api.graphql.query_builder import QueryBuilder
from src.api.graphql.query import Query
from src.apps.daostack.business.transfers.serie import Serie
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.data_access.graphql.dao_stacked_serie.\
    dao_stacked_serie_interface import DaoStackedSerieInterface
from src.app import DEBUG
from src.logs import LOGS


METRIC_TYPE_NEW_USERS: int = 0
METRIC_TYPE_NEW_PROPOSAL: int = 1

class DaoSimpleTimeSerieMetric(DaoStackedSerieInterface):
    def __init__(self, m_type: int, ids: List[str], requester):
        self.__m_type = self.__get_key_from_type(m_type)
        self.__ids = ids
        self.__requester = requester


    def __get_key_from_type(self, m_type: int) -> str:
        m_key: str = ''
        if m_type == METRIC_TYPE_NEW_USERS:
            m_key = 'reputationHolders'
        elif m_type == METRIC_TYPE_NEW_PROPOSAL:
            m_key = 'proposals'

        return m_key


    def __get_query(self, n_first: int, n_skip: int, o_id: int):
        return Query(
                    header = 'dao',
                    body = Query(
                                header = self.__m_type,
                                body = ['createdAt'],
                                filters = {
                                    'first': f'{n_first}',
                                    'skip': f'{n_skip}',
                                },
                            ),
                    filters = {
                        'id': f'\"{o_id}\"',
                    })


    def __dict_to_df(self, columns: List[str], data: List) -> pd.DataFrame:
        """
        Takes data and transforms it in a data frame which is returned.
        """
        df: pd.DataFrame = pd.DataFrame(columns = columns)

        for di in data:
            serie: pd.Series = pd.Series([di['createdAt']], index=df.columns)
            df = df.append(serie, ignore_index=True)

        return df


    def __request(self, o_id: str, columns: List[str]) -> pd.DataFrame:
        chunk: int = 0
        result: Dict[str, List] = dict()
        df: pd.DataFrame = pd.DataFrame(columns=columns)
        condition: bool = True

        while condition:
            e_chunk = self.__requester.get_elems_per_chunk(chunk)
            query: Query = self.__get_query(n_first=e_chunk, n_skip=df.shape[0], 
                o_id=o_id)
            q_builder: QueryBuilder = QueryBuilder([query])

            result = self.__requester.request(q_builder.build())
            result = result['dao'][self.__m_type]

            dff: pd.DataFrame = self.__dict_to_df(columns=columns, data=result)
            df = df.append(dff, ignore_index = True)

            condition = len(result) == e_chunk
            chunk += 1

        return df


    def __process_data(self, df: pd.DataFrame) -> StackedSerie:
        if df.shape[0] == 0:
            return StackedSerie()
        
        # takes just the month
        df['date'] = pd.to_datetime(df['date'], unit='s').dt.to_period('M')

        # counts how many month/year are repeated
        df = df.groupby(df['date']).size().reset_index(name='count')
        df['date'] = df['date'].dt.to_timestamp()
        
        # generates a time series
        today = datetime.now()
        today = datetime(today.year, today.month, 1)
        start = df['date'].min() if len(df['date']) > 0 else today 
        end = today
        idx = pd.date_range(start=start, end=end, freq=DateOffset(months=1))

        # joinning all the data in a unique dataframe
        dff = pd.DataFrame({'date': idx})
        dff['count'] = 0
        df = df.append(dff, ignore_index = True)
        df.drop_duplicates(subset='date', keep="first", inplace = True)
        df.sort_values('date', inplace = True)

        serie: Serie = Serie(x = df['date'].tolist())
        metric: StackedSerie = StackedSerie(
            serie = serie, 
            y_stack = [df['count'].tolist()])

        return metric


    def get_stacked_serie(self) -> StackedSerie:
        start: datetime = datetime.now()
        df: pd.DataFrame = pd.DataFrame(columns = ['date'])

        for o_id in self.__ids:
            dff: pd.DataFrame = self.__request(o_id=o_id, columns=df.columns)
            df = df.append(dff, ignore_index=True)

        if DEBUG:
            duration: int = (datetime.now() - start).total_seconds()
            print(LOGS['daos_requested'].format(len(self.__ids), duration))

        return self.__process_data(df)
