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

from api.api_manager import request
from apps.dashboard.domain.model_transfers import MetricNewUsers
from api.query_builder import QueryBuilder
from api.query import Query
from api.api_manager import ELEMS_PER_CHUNK
from app import DEBUG
from logs import LOGS


def get_new_users_metric(id: str) -> MetricNewUsers:
    """
    Gets a specific DAO's users metric.
    Params:
        id: the id of an existing DAO.
    Return:
        MetricNewUsers
    """
    chunks = 0
    result: Dict[str, List] = dict()
    members: List = list()
    start: datetime = datetime.now()

    while chunks == 0 or ('dao' in result and 
    len(result['dao']['reputationHolders']) == ELEMS_PER_CHUNK):

        q_builder: QueryBuilder = QueryBuilder()
        query: Query = Query(header = 'dao',
                             body = ['reputationHolders', '{createdAt}'], 
                             filters = {
                                'id': f'\"{id}\"',
                                'first': f'{ELEMS_PER_CHUNK + ELEMS_PER_CHUNK * chunks}',
                                'skip' : f'{ELEMS_PER_CHUNK * chunks}',
                             })
        q_builder.add_query(query)
        result = request(q_builder.build())
        chunks += 1
        members += result['dao']['reputationHolders']

    if not members:
        return MetricNewUsers()

    df: pd.DataFrame = pd.DataFrame([int(mem['createdAt']) 
        for mem in result['dao']['reputationHolders']], columns = ['date'])

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
    df = df.append(dff).sort_values('date').reset_index(drop=True)
    df = df.drop_duplicates(subset='date', keep="first")

    return MetricNewUsers(x=df['date'].tolist(), y=df['count'].tolist()) 