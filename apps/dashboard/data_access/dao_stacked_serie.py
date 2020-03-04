"""
   Descp: This is a dao (data access object) of stacked series.
    It's used in order to warp the transformation among
    API's responses and the App's transfer.  

   Created on: 26-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
import pandas as pd
from pandas.tseries.offsets import DateOffset
from datetime import datetime

from api.query_builder import QueryBuilder
from api.query import Query
import api.api_manager as api
from apps.dashboard.business.transfers.serie import Serie
from apps.dashboard.business.transfers.stacked_serie import StackedSerie 
from app import DEBUG
from logs import LOGS

METRIC_TYPE_NO_TYPE: int = 0
METRIC_TYPE_NEW_USERS: int = 1
METRIC_TYPE_NEW_PROPOSAL: int = 2


def __get_key_from_type(m_type: int) -> str:
    m_key: str = ''
    if m_type == METRIC_TYPE_NEW_USERS:
        m_key = 'reputationHolders'
    elif m_type == METRIC_TYPE_NEW_PROPOSAL:
        m_key = 'proposals'

    return m_key


def __request(o_id: str, m_type: int) -> List[int]:
    chunk: int = 0
    result: Dict[str, List] = dict()
    elems: List = list()
    start: datetime = datetime.now()
    m_key: str = __get_key_from_type(m_type)

    while chunk == 0 or ('dao' in result and \
    len(result['dao'][m_key]) == api.get_elems_per_chunk(chunk - 1)):

        q_builder: QueryBuilder = QueryBuilder()
        query: Query = Query(header = 'dao',
                            body = Query(
                                        header = m_key,
                                        body = ['createdAt'],
                                        filters = {
                                            'first': 
                                            f'{api.get_elems_per_chunk(chunk)}',
                                            'skip' : f'{len(elems)}',
                                        },
                                    ),
                            filters = {
                                'id': f'\"{o_id}\"',
                            })

        q_builder.add_query(query)
        result = api.request(q_builder.build())
        chunk += 1
        elems.extend([int(mem['createdAt']) for mem in result['dao'][m_key]])

    if DEBUG:
        print(LOGS['chunks_requested'].format(chunk, (datetime.now() - start)\
         .total_seconds() * 1000))

    return elems


def __process_data(data: List) -> StackedSerie:
    df: pd.DataFrame = pd.DataFrame(data, columns = ['date'])

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


def get_metric(ids: List[str], m_type: int = METRIC_TYPE_NO_TYPE) \
    -> StackedSerie:
    """
    Gets a stacked series metric from a type and a list of ids.
    Params:
        ids: a list of existing DAO's id.
        m_type: metric's type
    Return:
        StackedSerie
    """
    start: datetime = datetime.now()
    elems: List = list()

    for o_id in ids:
        elems.extend(__request(o_id = o_id, m_type = m_type))

    if DEBUG:
        duration: int = (datetime.now() - start).total_seconds()
        print(LOGS['daos_requested'].format(len(ids), duration))

    return __process_data(elems)