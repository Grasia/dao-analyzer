"""
   Descp: Bar chart layout used to wrap its representation.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import Dict
import plotly.graph_objs as go

from src.apps.daostack.presentation.charts.chart_layout import ChartLayout
from src.apps.daostack.presentation.charts.chart_configuration\
.chart_configuration import ChartConfiguration


class BarLayout(ChartLayout):

    def __init__(self) -> None:
        self.__configuration = ChartConfiguration()


    def get_empty_layout(self) -> Dict:
        return { 'data': [] }


    def get_layout(self, plot_data: Dict) -> Dict:
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
                x = plot_data['x'],
                y = plot_data['y'],
                name = plot_data['name'],
                marker_color = plot_data['color'])

        x_args: Dict = {
            'tickvals': plot_data['x'],
            'type': plot_data['type'],
            'tickformat': plot_data['x_format'],
            'tickangle': True,
            }

        y_args: Dict = {'grid': True}

        layout: go.Layout = go.Layout(
            xaxis = self.__configuration.get_axis_layout(args=x_args),
            yaxis = self.__configuration.get_axis_layout(args=y_args),
            legend = self.__configuration.get_legend(),
            shapes = self.__configuration.get_shapes(),
        )

        return {'data': bar, 'layout': layout}


    def get_configuration(self) -> ChartConfiguration:
        return self.__configuration
