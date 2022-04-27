"""
   Descp: Interface which must implement all metric strategies.

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Any
from pandas import DataFrame


class IMetricStrategy(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'clean_df') and
                callable(subclass.clean_df) and
                hasattr(subclass, 'process_data') and
                callable(subclass.process_data) or
                NotImplemented)


    @abc.abstractmethod
    def clean_df(self, df: DataFrame) -> DataFrame:
        """
        Removes unused columns from df.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def process_data(self, df: DataFrame) -> Any:
        """
        Proces and transform the data frame in a transfer class.
        Return: StackedSerie or NStackedSerie
        """
        raise NotImplementedError
