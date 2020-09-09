"""
    Descp: Bar chart layout used to wrap its representation.

    Created on: 09-sep-2020

    Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from src.apps.daostack.presentation.charts.chart_layout import ChartLayout


class BarLayout(ChartLayout):

    def __init__(self, title: str) -> None:
        self.__title = title


     def get_empty_layout(self) -> Any:
        """
        Returns an empty layout. 
        """
        raise NotImplementedError


    def get_layout(self, plot_data: Dict) -> Any:
        """
        Returns the chart layout filled with the plot_data argument.
        Note: see each implementation to know how plot_data structure is.
        """
        raise NotImplementedError
