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

import api.api_manager as api
from apps.dashboard.domain.transfers import MetricTimeSeries
from api.query_builder import QueryBuilder
from api.query import Query
from app import DEBUG
from logs import LOGS


def get_new_users_metric(id: str) -> MetricTimeSeries:
    """
    Gets a specific DAO's new users metric.
    Params:
        id: the id of an existing DAO.
    Return:
        MetricTimeSeries
    """
    chunk = 0
    result: Dict[str, List] = dict()
    members: List = list()
    start: datetime = datetime.now()

    while chunk == 0 or ('dao' in result and \
    len(result['dao']['reputationHolders']) == \
    api.get_elems_per_chunk(chunk - 1)):

        q_builder: QueryBuilder = QueryBuilder()
        query: Query = Query(header = 'dao',
                             body = Query(
                                        header = 'reputationHolders',
                                        body = ['createdAt'],
                                        filters = {
                                            'first': f'{api.get_elems_per_chunk(chunk)}',
                                            'skip' : f'{len(members)}',
                                        },
                                    ),
                             filters = {
                                'id': f'\"{id}\"',
                             })

        q_builder.add_query(query)
        result = api.request(q_builder.build())
        chunk += 1
        members.extend(result['dao']['reputationHolders'])

    if DEBUG:
        print(LOGS['chunks_requested'].format(chunk, (datetime.now() - start)\
         .total_seconds() * 1000))

    df: pd.DataFrame = pd.DataFrame([int(mem['createdAt']) for mem in members],
     columns = ['date'])

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