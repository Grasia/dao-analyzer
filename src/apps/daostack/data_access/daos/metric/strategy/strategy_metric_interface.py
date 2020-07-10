"""
   Descp: Interface which must implement all metric strategies.

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import List, Dict, Any
from pandas import DataFrame

from src.apps.api.graphql.query import Query


class StrategyInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_empty_df') and
                callable(subclass.get_empty_df) and
                hasattr(subclass, 'process_data') and
                callable(subclass.process_data) and
                hasattr(subclass, 'get_query') and
                callable(subclass.get_query) and
                hasattr(subclass, 'fetch_result') and
                callable(subclass.fetch_result) and
                hasattr(subclass, 'dict_to_df') and
                callable(subclass.dict_to_df) or
                NotImplemented)


    @abc.abstractmethod
    def get_empty_df(self) -> DataFrame:
        raise NotImplementedError


    @abc.abstractmethod
    def process_data(self, df: DataFrame) -> Any:
        """
        Proces and transform the data frame in a transfer class.
        Return: StackedSerie or NStackedSerie
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_query(self, n_first: int, n_skip: int, o_id: int) -> Query:
        raise NotImplementedError


    @abc.abstractmethod
    def fetch_result(self, result: Dict) -> List:
        raise NotImplementedError


    @abc.abstractmethod
    def dict_to_df(self, data: List) -> DataFrame:
        """
        Takes data and transforms it in a data frame which is returned.
        """
        raise NotImplementedError
