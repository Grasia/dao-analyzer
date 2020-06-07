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

from src.app import DEBUG
from src.logs import LOGS


class ApiRequester:
    # Test the API in: https://thegraph.com/explorer/subgraph/daostack/master
    __DAOSTACK_URL = 'https://api.thegraph.com/subgraphs/name/daostack/master'
    __ELEMS_PER_CHUNK = 100


    def __init__(self):
        self.__client = GraphQLClient(self.__DAOSTACK_URL)


    def request(self, query: str) -> Dict[str, List]:
        """
        Requests querys at the endpoint.
        Return:
            The response as a dict, if an error ocurrs or theres no response 
            returns a empty dict. 
        """
        start: datetime

        if DEBUG:
            print(LOGS['request_to'].format(self.__DAOSTACK_URL))
            start = datetime.now()

        result = self.__client.execute(query)

        if DEBUG:
            print(LOGS['requested_in'].format((datetime.now() - start)
            .total_seconds() * 1000))

        result = json.loads(result)

        return result['data'] if 'data' in result else dict()


    def get_elems_per_chunk(self, n_chunk: int) -> int:
        elems: int = self.__ELEMS_PER_CHUNK * pow(2, n_chunk)
        # max elems per chunk = 1000
        return elems if elems <= 1000 else 1000