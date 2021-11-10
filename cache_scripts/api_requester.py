"""
   Descp: Functions to fetch from endpoint given queries.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from gql import Client
from gql.dsl import DSLQuery, DSLSchema, DSLType, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
from functools import partial

import config
import logging
import sys
from tqdm import tqdm
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
    def __init__(self, endpoint: str, pbar_enabled: bool=True) -> None:
        self.__transport = RequestsHTTPTransport(endpoint)
        self.__client: Client = Client(transport=self.__transport, fetch_schema_from_transport=True)
        self.pbar_enabled = pbar_enabled
        
        ## TODO: Maybe a tqdm wrapper would be better...
        if pbar_enabled:
            self.pbar = partial(tqdm, delay=1, total=0xffff, file=sys.stdout,
                desc="Requesting", bar_format="{l_bar}{bar}[{elapsed}<{remaining}]")
        else:
            ## TODO: Make some kind of simple spinner
            self.pbar = partial(tqdm, disable=True)

        logging.debug(f"Invoked ApiRequester with endpoint: {endpoint}")

    def get_schema(self) -> DSLSchema:
        with self.__client as _:
            assert(self.__client.schema is not None)
            return DSLSchema(self.__client.schema)

    def request(self, query: DSLQuery) -> Dict:
        """
        Requests data from endpoint.
        """
        logging.debug(f"Requesting: {query}")
        result = self.__client.execute(dsl_gql(query))
        if "errors" in result:
            raise ApiQueryException(result["errors"])

        return result

    def _update_pbar(self, pbar, last_index:str):
        if self.pbar_enabled and last_index:
            pbar.update(int(last_index[:6], 0) - pbar.n)
        elif not self.pbar_enabled:
            ## TODO: Advance spinner
            pass

    def n_requests(self, query:DSLType, result_key: str, index='id', last_index: str = "") -> List[Dict]:
        """
        Requests all chunks from endpoint.

        Parameters:
            * query: json to request
            * skip_n: number of rows to skip
            * result_key: dict key to access the list
            * index: dict key to use as index
            * last_index: used to continue the request
            * pbar_enabled: wether to enable the progress bar or just display messages
        """
        elements: List[Dict] = list()
        result = Dict
        
        # do-while structure
        exit: bool = False

        with self.pbar() as pbar:
            while not exit:
                q: DSLQuery = DSLQuery(query(where={index+"_gt": last_index}))

                try:
                    result = self.request(q)
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
                    self._update_pbar(pbar, last_index)
                    last_index = result[-1][index]
                else:
                    if self.pbar_enabled:
                        pbar.update(pbar.total - pbar.n)
                    ## TODO: Else finish the pbar thingie
                    exit = True

        return elements
