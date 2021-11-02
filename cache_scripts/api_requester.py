"""
   Descp: Functions to fetch from endpoint given queries.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import json

from gql.dsl import DSLQuery, DSLSchema, dsl_gql
import config
import logging
from graphqlclient import GraphQLClient
from typing import Callable, Dict, List


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

    def request(self, query: DSLQuery) -> Dict:
        """
        Requests data from endpoint.
        """
        logging.debug(f"Requesting: {query}")
        result = json.loads(self.__client.execute(query))
        if "errors" in result:
            raise ApiQueryException(result["errors"])

        return result['data'] if 'data' in result else dict()

    def n_requests(self, build_query, result_key: str, index='id', last_index: str = "") -> List[Dict]:
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

        with self.client as session:
            assert(self.client.schema is not None)
            ds: DSLSchema = DSLSchema(self.client.schema)

        while not exit:
            q: DSLQuery = DSLQuery(build_query(ds, where={index+"_gt": last_index}))

            try:
                result = self.request(session, q)
                if not result:
                    logging.warning("Request returned no results")
                result = result[result_key]
            except KeyError as k:
                if config.ignore_errors:
                    logging.error("Could not find keys: " + ",".join(k.args))
                    break
                else:
                    raise k
            except Exception as e:
                if config.ignore_errors:
                    logging.exception(e)
                    break
                else:
                    raise e

            elements.extend(result)

            # if return data (result) has no elements, we have finished
            if result: 
                assert(last_index != result[-1][index])
                last_index = result[-1][index]
            else:
                exit = True

        return elements
