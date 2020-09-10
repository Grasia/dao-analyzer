"""
   Descp: Chart interface which has to implement every chart type.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Any

from src.apps.daostack.presentation.charts.chart_configuration\
.chart_configuration import ChartConfiguration

class Chart(metaclass=abc.ABCMeta):

    ID: int = 0

    def __init__(self) -> None:
        Chart.ID += 1


    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_layout') and
                callable(subclass.get_layout) and
                hasattr(subclass, 'get_layout_configuration') and
                callable(subclass.get_layout_configuration) and
                hasattr(subclass, 'enable_subtitles') and
                callable(subclass.enable_subtitles) and
                hasattr(subclass, 'disable_subtitles') and
                callable(subclass.disable_subtitles) or
                NotImplemented)

    
    @abc.abstractmethod
    def get_layout(self) -> Any:
        """
        Returns an empty layout. 
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_layout_configuration(self) -> ChartConfiguration:
        """
        Returns the layout configuration.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def enable_subtitles(self) -> ChartConfiguration:
        """
        Enables the pane subtitles.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def disable_subtitles(self) -> ChartConfiguration:
        """
        Disables the pane subtitles. 
        """
        raise NotImplementedError
