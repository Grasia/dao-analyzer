"""
   Descp: Strategy pattern for create simple metrics based on time series.

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict
import pandas as pd
from pandas.tseries.offsets import DateOffset
from datetime import date

from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
        strategy_metric_interface import StrategyInterface

from src.api.graphql.query import Query
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.serie import Serie


METRIC_TYPE_NEW_USERS: int = 0
METRIC_TYPE_NEW_PROPOSAL: int = 1


class StTimeSerie(StrategyInterface):
    def __init__(self, m_type: int):
        self.__m_type = self.__get_type(m_type)


    def __get_type(self, m_type: int) -> str:
        m_key: str = ''
        if m_type == METRIC_TYPE_NEW_USERS:
            m_key = 'reputationHolders'
        elif m_type == METRIC_TYPE_NEW_PROPOSAL:
            m_key = 'proposals'

        return m_key


    def get_empty_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=['date'])


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if df.shape[0] == 0:
            return StackedSerie()
        
        # takes just the month
        df['date'] = pd.to_datetime(df['date'], unit='s').dt.date
        df['date'] = df['date'].apply(lambda d: d.replace(day=1))

        # counts how many month/year are repeated
        df = df.groupby(df['date']).size().reset_index(name='count')
        
        # generates a time series
        today = date.today().replace(day=1)
        start = df['date'].min()
        idx = pd.date_range(start=start, end=today, freq=DateOffset(months=1))

        # joinning all the data in a unique dataframe
        dff = pd.DataFrame({'date': idx})
        dff['date'] = dff['date'].dt.date
        dff['count'] = 0
        df = df.append(dff, ignore_index=True)
        df.drop_duplicates(subset='date', keep="first", inplace=True)
        df.sort_values('date', inplace=True)
        
        serie: Serie = Serie(x=df['date'].tolist())
        metric: StackedSerie = StackedSerie(
            serie = serie, 
            y_stack = [df['count'].tolist()])

        return metric


    def get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
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


    def fetch_result(self, result: Dict) -> List:
        return result['dao'][self.__m_type]

    
    def dict_to_df(self, data: List) -> pd.DataFrame:
        df: pd.DataFrame = self.get_empty_df()

        for di in data:
            serie: pd.Series = pd.Series([di['createdAt']], index=df.columns)
            df = df.append(serie, ignore_index=True)

        return df
