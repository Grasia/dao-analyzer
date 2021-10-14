"""
   Descp: Functions to fetch from endpoint given queries.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import json
import config
import logging
from graphqlclient import GraphQLClient
from typing import Dict, List


class ApiQueryException(Exception):
    def __init__(self, errors, msg="Errors in GraphQL Query"):
        super().__init__(msg)
        self.__errors = errors

    def errorsString(self) -> str:
        return '\n'.join([f"> {e['message']}" for e in self.__errors])

    def __str__(self):
        return super().__str__() + ":\n" + self.errorsString()


class ApiRequester:

    ELEMS_PER_CHUNK: int = 1000

    def __init__(self, endpoint: str) -> None:
        self.__client: GraphQLClient = GraphQLClient(endpoint)
        logging.debug(f"Invoked ApiRequester with endpoint: {endpoint}")

    def request(self, query: str) -> Dict:
        """
        Requests data from endpoint.
        """
        result = json.loads(self.__client.execute(query))
        if "errors" in result:
            raise ApiQueryException(result["errors"])

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
        exit: bool = False

        while not exit:
            query_filled: str = query.format(self.ELEMS_PER_CHUNK, skip_n + len(elements))
            logging.debug(f"Requesting: {query_filled}")

            try:
                result = self.request(query=query_filled)
                if not result:
                    logging.warning("Request returned no results")
                result = result[result_key]
            except KeyError as k:
                if config.ignore_errors:
                    logging.error("Could not find keys: " + ",".join(k.args))
                else:
                    raise k
            except Exception as e:
                if config.ignore_errors:
                    logging.exception(e)
                    return elements
                else:
                    raise e

            elements.extend(result)

            # if return data (result) has less than ELEMS_PER_CHUNK means that it was the last chunk 
            exit = len(result) <= self.ELEMS_PER_CHUNK

        return elements
