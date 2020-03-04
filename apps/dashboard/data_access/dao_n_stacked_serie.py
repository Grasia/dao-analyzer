"""
   Descp: This is a dao (data access object) of n stacked series.
    It's used in order to warp the transformation among
    API's responses and the App's transfer.  

   Created on: 4-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
from pandas.tseries.offsets import DateOffset
from datetime import datetime
import pandas as pd

from app import DEBUG
from logs import LOGS
from apps.dashboard.business.transfers.n_stacked_serie import NStackedSerie
from api.query import Query
from api.query_builder import QueryBuilder
import api.api_manager as api


def __apend_data(dict1: Dict[str, List], dict2):
    """
    Takes dict2 key-val elements and puts them into dict1
    """
    for e in dict2:
        for k in e:
            dict1[k].append(e[k])


def __request(o_id: str) -> Dict[str, List]:
    chunk: int = 0
    result: Dict[str, List] = dict()
    elems: Dict[str, List] = {
        'closingAt': list(),
        'boostedAt': list(),
        'winningOutcome': list()
    }
    start: datetime = datetime.now()

    while chunk == 0 or ('dao' in result and \
    len(result['dao']['proposals']) == api.get_elems_per_chunk(chunk - 1)):

        q_builder: QueryBuilder = QueryBuilder()
        query: Query = Query(header = 'dao',
                            body = Query(
                                        header = 'proposals',
                                        body = ['closingAt', 'boostedAt', 'winningOutcome'],
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
        __apend_data(dict1 = elems, dict2 = result['dao']['proposals'])
        chunk += 1

    if DEBUG:
        print(LOGS['chunks_requested'].format(chunk, (datetime.now() - start)\
         .total_seconds() * 1000))

    int_parser = lambda x: int(x)
    bool_parser = lambda x: True if x == 'Pass' else False

    map(int_parser, elems['closingAt'])
    map(int_parser, elems['boostedAt'])
    map(bool_parser, elems['winningOutcome'])

    return elems


def __process_data(data: Dict[str, List]) -> NStackedSerie:
    df: pd.DataFrame = pd.DataFrame.from_dict(data)

    # takes just the month
    df['closingAt'] = pd.to_datetime(df['closingAt'], unit='s').dt.to_period('M')
    df['boostedAt'] = pd.to_datetime(df['boostedAt'], unit='s').dt.to_period('M')
    print(df)

    # # counts how many month/year are repeated
    # df = df.groupby(df['date']).size().reset_index(name='count')
    # df['date'] = df['date'].dt.to_timestamp()
    
    # # generates a time series
    # today = datetime.now()
    # today = datetime(today.year, today.month, 1)
    # start = df['date'].min() if len(df['date']) > 0 else today 
    # end = today
    # idx = pd.date_range(start=start, end=end, freq=DateOffset(months=1))

    # # joinning all the data in a unique dataframe
    # dff = pd.DataFrame({'date': idx})
    # dff['count'] = 0
    # df = df.append(dff, ignore_index = True)
    # df.drop_duplicates(subset='date', keep="first", inplace = True)
    # df.sort_values('date', inplace = True)

    # serie: Serie = Serie(x = df['date'].tolist())
    # metric: StackedSerie = StackedSerie(
    #     serie = serie, 
    #     y_stack = [df['count'].tolist()])

    # return metric


def get_metric(ids: List[str]) -> NStackedSerie:
    """
    Gets a n times stacked serie from a list of ids.
    Params:
        ids: a list of existing DAO's id.
    Return:
        NStackedSerie
    """
    start: datetime = datetime.now()
    elems: Dict[str, List] = dict()

    for o_id in ids:
        __apend_data(dict1 = elems, dict2 = __request(o_id = o_id))

    if DEBUG:
        duration: int = (datetime.now() - start).total_seconds()
        print(LOGS['daos_requested'].format(len(ids), duration))

    return __process_data(elems)
