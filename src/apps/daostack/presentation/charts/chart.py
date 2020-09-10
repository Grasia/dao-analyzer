"""
   Descp: Chart interface which has to implement every chart type.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Any


class Chart(metaclass=abc.ABCMeta):

    ID: int = 0

    def __init__(self) -> None:
        Chart.ID += 1


    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_layout') and
                callable(subclass.get_layout) or
                NotImplemented)

    
    @abc.abstractmethod
    def get_layout(self) -> Any:
        """
        Returns an empty layout. 
        """
        raise NotImplementedError
