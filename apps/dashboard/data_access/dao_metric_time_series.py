"""
   Descp: This is a dao (data access object) of new user metric.
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
from apps.dashboard.business.transfers import MetricTimeSeries
from app import DEBUG
from logs import LOGS


def __get_key_from_type(o_type: int) -> str:
    o_key: str = ''
    if o_type == MetricTimeSeries.METRIC_TYPE_NEW_USERS:
        o_key = 'reputationHolders'
    elif o_type == MetricTimeSeries.METRIC_TYPE_NEW_PROPOSAL:
        o_key = 'proposals'

    return o_key


def __request(o_id: str, o_type: int) -> List:
    chunk: int = 0
    result: Dict[str, List] = dict()
    elems: List = list()
    start: datetime = datetime.now()
    o_key: str = __get_key_from_type(o_type)

    while chunk == 0 or ('dao' in result and \
    len(result['dao'][o_key]) == api.get_elems_per_chunk(chunk - 1)):

        q_builder: QueryBuilder = QueryBuilder()
        query: Query = Query(header = 'dao',
                            body = Query(
                                        header = o_key,
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
        elems.extend([int(mem['createdAt']) for mem in result['dao'][o_key]])

    if DEBUG:
        print(LOGS['chunks_requested'].format(chunk, (datetime.now() - start)\
         .total_seconds() * 1000))

    return elems


def __process_data(l_dates: List) -> MetricTimeSeries:
    df: pd.DataFrame = pd.DataFrame(l_dates, columns = ['date'])

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

    metric: MetricTimeSeries = MetricTimeSeries(
        x = df['date'].tolist(), 
        y = df['count'].tolist(),
        m_type = MetricTimeSeries.METRIC_TYPE_NEW_USERS)

    return metric


def get_metric(ids: List[str], 
o_type: int = MetricTimeSeries.METRIC_TYPE_NO_TYPE) -> MetricTimeSeries:
    """
    Gets a time series metric from a type and a list of ids.
    Params:
        ids: a list of existing DAO's id.
        o_type: metric's type
    Return:
        MetricTimeSeries
    """
    start: datetime = datetime.now()
    elems: List = list()

    for o_id in ids:
        elems.extend(__request(o_id = o_id, o_type = o_type))

    if DEBUG:
        duration: int = (datetime.now() - start).total_seconds()
        print(LOGS['daos_requested'].format(len(ids), duration))

    return __process_data(elems)