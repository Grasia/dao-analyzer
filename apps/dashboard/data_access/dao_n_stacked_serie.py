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


def __transform_json(result: Dict, elements: Dict[str, List]):
    """
    Takes result key-val elements and puts them into elems
    """
    for k in result:
        for e in result[k]:
            elements[k] = e


def __request(o_id: str) -> Dict[str, List]:
    chunk: int = 0
    result: Dict[str, List] = dict()
    elems: Dict[str, List] = dict()
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
        __transform_json(result = result, elements = elems)
        chunk += 1

    if DEBUG:
        print(LOGS['chunks_requested'].format(chunk, (datetime.now() - start)\
         .total_seconds() * 1000))

    return elems


def get_metric(ids: List[str]) -> NStackedSerie:
    """
    Gets a n times stacked serie from a list of ids.
    Params:
        ids: a list of existing DAO's id.
    Return:
        NStackedSerie
    """
    start: datetime = datetime.now()
    elems: List = list()

    for o_id in ids:
        elems.extend(__request(o_id = o_id))

    if DEBUG:
        duration: int = (datetime.now() - start).total_seconds()
        print(LOGS['daos_requested'].format(len(ids), duration))

    return __process_data(elems)
