"""
   api_manager.py

   Descp: This file its used to warp all the GraphQL API interactions.

   Created on: 21-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import json
from datetime import datetime
from graphqlclient import GraphQLClient

from app import DEBUG

# Test the API in: https://thegraph.com/explorer/subgraph/daostack/master
DAOSTACK_URL = 'https://api.thegraph.com/subgraphs/name/daostack/master'

daostack_client = GraphQLClient(DAOSTACK_URL)

def __request(query: str) -> dict:
    """
    Requests querys at the endpoint
    Return:
        The response as a dict, if an error ocurrs returns a empty dict 
    """
    start: datetime
    if DEBUG:
        print(f'Requesting to: {DAOSTACK_URL}')
        start = datetime.now()

    result = daostack_client.execute(query)

    if DEBUG:
        print(f'Requested in: \
            {(datetime.now() - start).total_seconds() * 1000.0 :.4f} ms')

    result = json.loads(result)

    return result['data'] if 'data' in result else dict()


def get_all_daos() -> list:
    """
    Requests all the DAOs name
    Return:
        A list filled with DAOs name
    """
    query: str = '''
    {
        daos {
            name
        }
    }
    '''
    daos: list = __request(query)
    return [obj['name'] for obj in daos['daos']]