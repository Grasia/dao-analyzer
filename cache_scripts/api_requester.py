"""
   Descp: Functions to fetch from endpoint given queries.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from gql import Client
from gql.dsl import DSLField, DSLQuery, DSLSchema, DSLType, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
import re

import logging
import sys
from tqdm import tqdm
from typing import Dict, List, Union

class ApiQueryException(Exception):
    def __init__(self, errors, msg="Errors in GraphQL Query"):
        super().__init__(msg)
        self.__errors = errors

    def errorsString(self) -> str:
        return '\n'.join([f"> {e['message']}" for e in self.__errors])

    def __str__(self):
        return super().__str__() + ":\n" + self.errorsString()

class IndexProgressBar(tqdm):
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
        self.toFinish = False
        self.total = 0

    def progress(self, last_index: str, new_items: int):
        filler = " " * max(0, len(self.prev_lastindex) - len(last_index))
        self.total += new_items
        print(f"Requesting... Total: {self.total:5d}. Requested until {last_index}"+filler, end='\r', flush=True)
        self.prev_lastindex = last_index
        self.toFinish = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # To remove the last \r
        if self.toFinish:
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

    def request(self, query: Union[DSLQuery, DSLField]) -> Dict:
        """
        Requests data from endpoint.
        """
        if isinstance(query, DSLField):
            query = DSLQuery(query)

        logging.debug(f"Requesting: {query}")
        result = self.__client.execute(dsl_gql(query))
        if "errors" in result:
            raise ApiQueryException(result["errors"])

        return result

    def request_single(self, q: Union[DSLQuery, DSLField]) -> Dict:
        result = self.request(q)
        if result and len(result.values()) == 1:
            return next(iter(result.values()))
        else:
            raise 

    def n_requests(self, query:DSLType, index='id', last_index: str = "", block_hash: str = None) -> List[Dict]:
        """
        Requests all chunks from endpoint.

        Parameters:
            * query: json to request
            * index: dict key to use as index
            * last_index: used to continue the request
            * block_hash: make the request to that block hash
        """
        elements: List[Dict] = list()
        result = Dict
        
        # do-while structure
        exit: bool = False

        with self.pbar() as pbar:
            while not exit:
                query_args = {
                    "where": {index+"_gt": last_index},
                    "first": self.ELEMS_PER_CHUNK
                }
                if block_hash:
                    query_args["block"] = {"hash": block_hash}

                result = self.request_single(query(**query_args))
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
