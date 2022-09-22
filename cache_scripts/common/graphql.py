import logging
from typing import Callable, List, Dict
from abc import ABC, abstractmethod

import pandas as pd

from gql.dsl import DSLField

from .common import ENDPOINTS, NetworkCollector, NetworkRunner, Runner, UpdatableCollector
from .api_requester import GQLRequester
from ..metadata import Block

def add_where(d, **kwargs):
    """
    Adds the values specified in kwargs to the where inside d
        Example: `**add_where(kwargs, deleted=False)`
    """
    if "where" in d:
        d["where"] |= kwargs
    else:
        d["where"] = kwargs
    
    return d

def partial_query(q, w) -> DSLField:
    def wrapper(**kwargs):
        return q(**add_where(kwargs, **w))
    return wrapper

def checkSubgraphHealth(endpoint: str, network: str = None):
    subgraphName = '/'.join(endpoint.split('/')[-2:])
    
    requester = GQLRequester(endpoint=ENDPOINTS['_theGraph']['index-node'], introspection=False)
    q = f"""
    {{
        indexingStatusForCurrentVersion(subgraphName: "{subgraphName}") {{
            health,
            synced,
            node,
            chains {{
                network
            }}
        }}
    }}
    """

    r = requester.request_single(q)

    if not r['synced']:
        logging.info(f"Subgraph {endpoint} is not synced")

    if r['health'].lower() != 'healthy':
        logging.error(f"Subgraph {endpoint} is not healthy")
        return False
    
    subgraph_network = r['chains'][0]['network']
    if network and subgraph_network != network:
        logging.error(f"Subgraph {endpoint} expected network {network} but got {subgraph_network}")
        return False

    return True

class GraphQLCollector(NetworkCollector, UpdatableCollector):
    def __init__(self, name: str, runner: Runner, endpoint: str, result_key: str = None, index: str = None, network: str='mainnet', pbar_enabled: bool=True):
        super().__init__(name, runner, network)
        self.endpoint: str = endpoint
        self.index = index if index else 'id'
        self.result_key = result_key if result_key else name
        self.postprocessors: Callable = []

        self.requester: GQLRequester = GQLRequester(endpoint=self.endpoint, pbar_enabled=pbar_enabled)

    def postprocessor(self, f: Callable[[pd.DataFrame], pd.DataFrame]):
        self.postprocessors.append(f)
        return f

    @property
    def schema(self):
        return self.requester.get_schema()

    @abstractmethod
    def query(self, **kwargs) -> DSLField:
        raise NotImplementedError

    @property
    def df(self) -> pd.DataFrame:
        if not self.data_path.is_file():
            return pd.DataFrame()

        df = pd.read_feather(self.data_path)
        if self.network:
            df = df[df['network'] == self.network]
        
        return df

    def transform_to_df(self, data: List[Dict], skip_post: bool=False) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(pd.json_normalize(data))

        # For compatibility reasons we change from . to snake case
        def dotsToSnakeCase(str: str) -> str:
            splitted = str.split('.')
            return splitted[0] + ''.join(x[0].upper()+x[1:] for x in splitted[1:])
                        
        df = df.rename(columns=dotsToSnakeCase)
        df['network'] = self.network

        if not skip_post:
            for post in self.postprocessors:
                logging.debug(f"Running postprocessor {post.__name__}")
                df = post(df)
                if df is None:
                    raise ValueError(f"The postprocessor {post.__name__} returned None")

        return df

    def verify(self) -> bool:
        # Checking if the queryBuilder doesn't raise any errors
        self.query()

        # Checking the health of the subgraph
        return checkSubgraphHealth(self.endpoint)

    def query_cb(self, prev_block: Block = None):
        if prev_block:
            return partial_query(self.query, {'_change_block': {'number_gte': prev_block.number}})
        else:
            return self.query

    def run(self, force=False, block: Block = None, prev_block: Block = None):
        logging.info(f"Running GraphQLCollector with block: {block}, prev_block: {prev_block}")
        if block is None:
            block = Block()
        if prev_block is None or force:
            prev_block = Block()

        data = self.requester.n_requests(query=self.query_cb(prev_block), block_hash=block.id)

        # transform to df
        df: pd.DataFrame = self.transform_to_df(data)
        self._update_data(df, force)

class GraphQLRunner(NetworkRunner, ABC):
    pass