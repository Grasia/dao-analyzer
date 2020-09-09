"""
   Descp: The interface of charts layout.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Any, Dict

class ChartLayout(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_empty_layout') and
                callable(subclass.get_empty_layout) and
                hasattr(subclass, 'get_layout') and
                callable(subclass.get_layout) or
                NotImplemented)

    
    @abc.abstractmethod
    def get_empty_layout(self) -> Any:
        """
        Returns an empty layout. 
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_layout(self, plot_data: Dict) -> Any:
        """
        Returns the chart layout filled with the plot_data argument.
        Note: see each implementation to know how plot_data structure is.
        """
        raise NotImplementedError
