"""
   Descp: The interface which each figure must implement.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Dict

from dao_analyzer.web.apps.common.presentation.charts.layout.figure.figure_configuration \
    import FigureConfiguration

class Figure(metaclass=abc.ABCMeta):


    def __init__(self) -> None:
        self.__configuration: FigureConfiguration = FigureConfiguration()


    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_empty_figure') and
                callable(subclass.get_empty_figure) and
                hasattr(subclass, 'get_figure') and
                callable(subclass.get_figure) and
                hasattr(subclass, 'get_empty_plot_data') and
                callable(subclass.get_empty_plot_data) or
                NotImplemented)

    
    @property
    def configuration(self) -> FigureConfiguration:
        return self.__configuration


    @abc.abstractmethod
    def get_empty_figure(self) -> Dict:
        """
        Returns an empty figure. 
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_figure(self, plot_data: Dict) -> Dict:
        """
        Returns the figure filled with the plot_data argument.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_empty_plot_data(self) -> Dict:
        """
        Returns an empty dictionary with the plot_data schema.
        """
        raise NotImplementedError
