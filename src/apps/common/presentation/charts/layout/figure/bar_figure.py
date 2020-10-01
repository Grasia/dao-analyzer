"""
   Descp: This class is used to represent a bar plot.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import Dict
import plotly.graph_objs as go

from src.apps.common.presentation.charts.layout.figure.figure import Figure
import src.apps.common.resources.colors as Color

class BarFigure(Figure):

    def __init__(self) -> None:
        super().__init__()


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
        super().configuration.disable_legend()

        layout: go.Layout = go.Layout(
            xaxis=super().configuration.get_axis_layout(args=x_args),
            yaxis=super().configuration.get_axis_layout(args=y_args),
            legend=super().configuration.get_legend(),
            shapes=super().configuration.get_shapes(),
        )

        return {'data': [bar], 'layout': layout}
