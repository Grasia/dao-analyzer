"""
   Descp: Functions to fetch from endpoint given queries.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from gql import Client
from gql.dsl import DSLQuery, DSLSchema, DSLType, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
import re

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

class IndexProgressBar(tqdm):
    ## TODO: Show total number of requests
    def __init__(self, total=0xffff):
        super().__init__(delay=1, total=total, file=sys.stdout, desc="Requesting",
            bar_format="{l_bar}{bar}[{elapsed}<{remaining}{postfix}]", dynamic_ncols=True,
            postfix={"requested":0})
        self.requested = 0

    def progress(self, last_index: str, new_items: int):
        self.requested += new_items
        self.set_postfix(refresh=False, requested=self.requested)

        if not last_index:
            last_index = "0x0"

        match = re.search(r"0x[\da-fA-F]+", last_index)
        if match:
            self.update(int(match[0][:6], 0) - self.n)
        else:
            raise ValueError(f"{last_index} doesn't contain any hex values")

    def complete(self):
        self.update(self.total - self.n)

class RequestProgressSpinner:
    def __init__(self):
        self.prev_lastindex = ""
        self.total = 0

    def progress(self, last_index: str, new_items: int):
        filler = " " * max(0, len(self.prev_lastindex) - len(last_index))
        self.total += new_items
        print(f"Requesting... Total: {self.total:5d}. Requested until {last_index}"+filler, end='\r', flush=True)
        self.prev_lastindex = last_index

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # To remove the last \r
        if self.prev_lastindex:
            print()

    def complete(self):
        pass

class ApiRequester:
    ELEMS_PER_CHUNK: int = 1000

    def __init__(self, endpoint: str, pbar_enabled: bool=True) -> None:
        self.__transport = RequestsHTTPTransport(endpoint)
        self.__client: Client = Client(transport=self.__transport, fetch_schema_from_transport=True)
        self.pbar = IndexProgressBar if pbar_enabled else RequestProgressSpinner

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

    def n_requests(self, query:DSLType, index='id', last_index: str = "") -> List[Dict]:
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

        ## TODO: Use the same already stablished block for all requests
        # instead of making each request on the lastest one (which can change)
        with self.pbar() as pbar:
            while not exit:
                q: DSLQuery = DSLQuery(query(where={index+"_gt": last_index}, first=self.ELEMS_PER_CHUNK))

                try:
                    result = self.request(q)
                    if not result:
                        logging.warning("Request returned no results")
                    elif len(result.values()) == 1:
                        result = next(iter(result.values()))
                    else:
                        logging.error("BEWARE! the request returned more than one result!")
                except KeyError as k:
                    if config.ignore_errors:
                        logging.error("Could not find keys: " + ",".join(k.args))
                        break
                    else:
                        raise k
                ## TODO: Treat 502 exceptions
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
                    pbar.progress(last_index=last_index, new_items=len(result))
                    last_index = result[-1][index]
                else:
                    pbar.complete()
                    exit = True

        return elements
