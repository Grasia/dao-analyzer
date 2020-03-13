"""
   Descp: Interface which must implement all dao stacked serie   

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import List

from src.apps.daostack.business.transfers.stacked_serie import StackedSerie

class DaoStackedSerieInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_stacked_serie') and
                callable(subclass.get_stacked_serie) or
                NotImplemented)


    @abc.abstractmethod
    def get_stacked_serie(self) -> StackedSerie:
        raise NotImplementedError
