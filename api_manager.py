"""
   Descp: This file its used to warp all the GraphQL API interactions.

   Created on: 21-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import json
from datetime import datetime
from typing import Dict, List
from graphqlclient import GraphQLClient

from app import DEBUG
from logs import LOGS

# Test the API in: https://thegraph.com/explorer/subgraph/daostack/master
DAOSTACK_URL = 'https://api.thegraph.com/subgraphs/name/daostack/master'
ELEMS_PER_CHUNK = 100

daostack_client = GraphQLClient(DAOSTACK_URL)

def request(query: str) -> Dict[str, List]:
    """
    Requests querys at the endpoint.
    Return:
        The response as a dict, if an error ocurrs or theres no response 
        returns a empty dict. 
    """
    start: datetime

    if DEBUG:
        print(LOGS['request_to'].format(DAOSTACK_URL))
        start = datetime.now()

    result = daostack_client.execute(query)

    if DEBUG:
        print(LOGS['requested_in'].format(1, (datetime.now() - start) \
         .total_seconds() * 1000))

    result = json.loads(result)

    return result['data'] if 'data' in result else dict()


def request_many(query: str, key: str):
    """
    Requests many times at the endpoint.
    Parameters:
        * query: a graphql query
        * key: a key to see whether there are still chunks to download
    Return:
        The response as a dict, if an error ocurrs or theres no response 
        returns a empty dict.
    """
    start: datetime
    chunks = 0

    if DEBUG:
        print(LOGS['request_to'].format(DAOSTACK_URL))
        start = datetime.now()

    result = daostack_client.execute(query)
    chunks += 1

    if DEBUG:
        print(LOGS['requested_in'].format(chunks, (datetime.now() - start) \
         .total_seconds() * 1000))

    result = json.loads(result)

    return result['data'] if 'data' in result else dict()