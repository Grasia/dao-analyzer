"""
   Descp: This is a dao (data access object) of stacked series.
    It's used in order to warp the transformation among
    API's responses and the App's transfer.  

   Created on: 4-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
from datetime import datetime
import pandas as pd

from src.app import DEBUG
from src.logs import LOGS
from src.apps.api.graphql.query import Query
from src.apps.api.graphql.query_builder import QueryBuilder
from src.apps.daostack.data_access.daos.metric.strategy.\
    strategy_metric_interface import StrategyInterface
from src.apps.daostack.data_access.requesters.api_requester import ApiRequester


class DaoStackedSerie():
    def __init__(self, ids: List[str], strategy: StrategyInterface,
     requester: ApiRequester):
        self.__ids = ids
        self.__st = strategy
        self.__requester = requester


    def __request(self, o_id: str) -> pd.DataFrame:
        """
        Requests data and returns a pandas dataframe with columns distribution.
        Params:
            * o_id = An organization id
        Return:
            * A pandas dataframe
        """
        chunk: int = 0
        result: Dict[str, List] = dict()
        df: pd.DataFrame = self.__st.get_empty_df()
        condition: bool = True

        while condition:
            e_chunk = self.__requester.get_elems_per_chunk(chunk)
            query: Query = self.__st.get_query(n_first=e_chunk, 
                n_skip=df.shape[0], o_id=o_id)
            q_builder: QueryBuilder = QueryBuilder([query])

            result = self.__requester.request(q_builder.build())
            result = self.__st.fetch_result(result)

            dff: pd.DataFrame = self.__st.dict_to_df(data=result)
            df = df.append(dff, ignore_index=True)

            condition = len(result) == e_chunk
            chunk += 1

        return df


    def get_metric(self):
        start: datetime = datetime.now()
        df: pd.DataFrame = self.__st.get_empty_df()

        for o_id in self.__ids:
            dff: pd.DataFrame = self.__request(o_id=o_id)
            df = df.append(dff, ignore_index=True)

        if DEBUG:
            duration: int = (datetime.now() - start).total_seconds()
            print(LOGS['daos_requested'].format(len(self.__ids), duration))

        return self.__st.process_data(df)
