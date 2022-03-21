from typing import Callable, List, Dict
from datetime import datetime
from abc import ABC, abstractmethod

import pandas as pd

from gql.dsl import DSLField

from .common import NetworkCollector, NetworkRunner, Runner
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

class GraphQLCollector(NetworkCollector):
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
                df = post(df)
                if df is None:
                    raise ValueError(f"The postprocessor {post.__name__} returned None")

        return df

    def verify(self) -> bool:
        self.query()
        return True

    def run(self, force=False, block: Block = None):
        if block is None:
            block = Block()

        data: List[Dict] = self.requester.n_requests(
            query=self.query,
            index=self.index,
            block_hash=block.id)

        # transform to df
        df: pd.DataFrame = self.transform_to_df(data)
        self._update_data(df, force)

class GraphQLUpdatableCollector(GraphQLCollector):
    DEFAULT_START_TEXT = "Updating data since {date}"
    DEFAULT_END_TEXT = "There are {len} new items"

    def run(self, force=False, *args, **kwargs):
        if not force and not self.df.empty:
            self.update(*args, **kwargs)
        else:
            super().run(force, *args, **kwargs)

    def _simple_timestamp(self, key: str = 'createdAt', block: Block = None, start_txt=DEFAULT_START_TEXT, end_txt=DEFAULT_END_TEXT, prev_df: pd.DataFrame = None):
        # 1. Get the max createdAt
        if prev_df is None:
            prev_df = self.df
        
        if prev_df.empty:
            return

        maxCreatedAt = int(prev_df[key].fillna(0).astype(int).max())
        print(start_txt.format(date=datetime.fromtimestamp(maxCreatedAt).isoformat()))

        # 2. Perform n_requests but with bigger createdAt than the max createdAt
        data = self.requester.n_requests(
            query=partial_query(self.query, {f"{key}_gte": maxCreatedAt}),
            block_hash=block.id)

        # 3. Update the file
        df = self.transform_to_df(data)
        print(end_txt.format(len=len(df)))
        self._update_data(df)

    def update(self, block: Block = None):
        self._simple_timestamp('createdAt', block)

class GraphQLRunner(NetworkRunner, ABC):
    pass