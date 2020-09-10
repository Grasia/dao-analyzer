"""
   Descp: The interface of charts layout.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Dict

from src.apps.daostack.presentation.charts.chart_configuration\
.chart_configuration import ChartConfiguration

class ChartLayout(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_empty_layout') and
                callable(subclass.get_empty_layout) and
                hasattr(subclass, 'get_layout') and
                callable(subclass.get_layout) and
                hasattr(subclass, 'get_configuration') and
                callable(subclass.get_configuration) and
                hasattr(subclass, 'get_empty_plot_data') and
                callable(subclass.get_empty_plot_data) or
                NotImplemented)

    
    @abc.abstractmethod
    def get_empty_layout(self) -> Dict:
        """
        Returns an empty layout. 
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_layout(self, plot_data: Dict) -> Dict:
        """
        Returns the chart layout filled with the plot_data argument.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_configuration(self) -> ChartConfiguration:
        """
        Returns the chart layout configuration.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_empty_plot_data(self) -> Dict:
        """
        Returns an empty dictionary with the plot_data schema.
        """
        raise NotImplementedError
