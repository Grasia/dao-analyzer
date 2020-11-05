"""
   Descp: The interface which each figure must implement.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Dict, List

from src.apps.common.presentation.charts.layout.figure.figure_configuration \
    import FigureConfiguration

class Figure(metaclass=abc.ABCMeta):


    def __init__(self, x_axis: int = 1, y_axis: int = 1) -> None:
        self.__configuration: FigureConfiguration = FigureConfiguration()
        self.__x_layout_params: List[Dict] = [{} for _ in range(x_axis)]
        self.__y_layout_params: List[Dict] = [{} for _ in range(y_axis)]


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


    def x_layout_params(self, axis: int = 0) -> Dict:
        return self.__x_layout_params[axis]


    def y_layout_params(self, axis: int = 0) -> Dict:
        return self.__y_layout_params[axis]


    def add_x_params(self, params: Dict, axis: int = 0) -> None:
        self.__add_params(params=params, axis=self.__x_layout_params[axis])


    def add_y_params(self, params: Dict, axis: int = 0) -> None:
        self.__add_params(params=params, axis=self.__y_layout_params[axis])


    def __add_params(self, params: Dict, axis: Dict) -> None:
        for k, v in params.items():
            axis[k] = v


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
