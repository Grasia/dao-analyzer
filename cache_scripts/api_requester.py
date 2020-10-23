"""
   Descp: Functions to fetch from endpoint given queries.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import json
from graphqlclient import GraphQLClient
from typing import Dict, List


class ApiRequester:

    ELEMS_PER_CHUNK: int = 1000

    DAOSTACK: int = 0
    DAOHAUS: int = 1
    ARAGON_MAINNET: int = 2
    ARAGON_TOKENS: int = 3
    ARAGON_VOTING: int = 4
    ARAGON_FINANCE: int = 5

    __URL_DAOSTACK: str = 'https://api.thegraph.com/subgraphs/name/daostack/master'
    __URL_DAOHAUS: str = 'https://api.thegraph.com/subgraphs/name/odyssy-automaton/daohaus'
    __URL_ARAGON_MAINNET: str = 'https://api.thegraph.com/subgraphs/name/aragon/aragon-mainnet'
    __URL_ARAGON_TOKENS: str = 'https://api.thegraph.com/subgraphs/name/aragon/aragon-tokens-mainnet'
    __URL_ARAGON_VOTING: str = 'https://api.thegraph.com/subgraphs/name/aragon/aragon-voting-mainnet'
    __URL_ARAGON_FINANCE: str = 'https://api.thegraph.com/subgraphs/name/aragon/aragon-finance-mainnet'


    def __init__(self, endpoint: int) -> None:
        url: str = self.__get_endpoint(endpoint)
        self.__client: GraphQLClient = GraphQLClient(url)


    def __get_endpoint(self, endpoint: int) -> str:
        url: str = ''

        if endpoint is self.DAOSTACK:
            url = self.__URL_DAOSTACK
        elif endpoint is self.DAOHAUS:
            url = self.__URL_DAOHAUS
        elif endpoint is self.ARAGON_MAINNET:
            url = self.__URL_ARAGON_MAINNET
        elif endpoint is self.ARAGON_TOKENS:
            url = self.__URL_ARAGON_TOKENS
        elif endpoint is self.ARAGON_VOTING:
            url = self.__URL_ARAGON_VOTING
        elif endpoint is self.ARAGON_FINANCE:
            url = self.__URL_ARAGON_FINANCE

        return url


    def request(self, query: str) -> Dict:
        """
        Requests data from endpoint.
        """
        result = self.__client.execute(query)
        result = json.loads(result)
        return result['data'] if 'data' in result else dict()


    def n_requests(self, query: str, skip_n: int, result_key: str) -> List[Dict]:
        """
        Requests all chunks from endpoint.

        Parameters:
            * query: json to request
            * skip_n: number of rows to skip
            * result_key: dict key to access the list
        """
        elements: List[Dict] = list()
        result = Dict
        
        # do-while structure
        condition: bool = True

        while condition:
            query_filled: str = query.format(self.ELEMS_PER_CHUNK, skip_n + len(elements))

            try:
                result = self.request(query=query_filled)
                result = result[result_key]
            except Exception:
                print('\nError: Not all elements was requested.\n')
                return elements

            elements.extend(result)

            # if return data (result) has less than ELEMS_PER_CHUNK means that it was the last chunk 
            condition = len(result) == self.ELEMS_PER_CHUNK

        return elements
