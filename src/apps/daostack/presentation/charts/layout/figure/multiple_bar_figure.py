"""
   Descp: This class is used to represent a multiple bar figure, this means,
        stacked multibar-bar figure, and grouped multi-bar figure.

   Created on: 14-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import Dict
import plotly.graph_objs as go

from src.apps.daostack.presentation.charts.layout.figure.figure import Figure
import src.apps.daostack.resources.colors as Color

class MultipleBarFigure(Figure):
    STACK: int = 0
    GROUP: int = 1
    __TYPE_STACK: str = 'stack'
    __TYPE_GROUP: str = 'group'


    def __init__(self, bar_type: int) -> None:
        super().__init__()
        self.__bar_type: str = self.__get_type(bar_type)


    def __get_type(self, bar_type: int) -> str:
        btype: str = self.__TYPE_GROUP

        if bar_type is self.STACK:
            bar_type = self.__TYPE_STACK

        return btype


    @staticmethod
    def get_empty_plot_data() -> Dict:
        return {
            'x': [],
            'y': [],
            'name': '',
            'color': Color.LIGHT_BLUE,
            'type': '-',
            'x_format': '',
        }


    def get_empty_figure(self) -> Dict:
        return self.get_figure(plot_data = self.get_empty_plot_data())


    def get_figure(self, plot_data: Dict) -> Dict:
        """
        Returns the bar chart filled with plot_data.
        Arguments:
            * plot_data = {
                'x': a list type filled with values.
                'y': a list type filled with values.
                'name': the name of the bar chart.
                'color': The bar's color.
                'type': The type of the x-axis values, e.g. date.
                'x_format': Format of the x-axis values, e.g. '%b, %Y'
            } 
        """
        bar: go.Bar = go.Bar(
                x=plot_data['x'],
                y=plot_data['y'],
                name=plot_data['name'],
                marker_color=plot_data['color'])

        x_args: Dict = {
            'tickvals': plot_data['x'],
            'type': plot_data['type'],
            'tickformat': plot_data['x_format'],
            'tickangle': True,
            }

        y_args: Dict = {'grid': True}

        layout: go.Layout = go.Layout(
            xaxis=self.__configuration.get_axis_layout(args=x_args),
            yaxis=self.__configuration.get_axis_layout(args=y_args),
            legend=self.__configuration.get_legend(),
            shapes=self.__configuration.get_shapes(),
        )

        return {'data': [bar], 'layout': layout}
