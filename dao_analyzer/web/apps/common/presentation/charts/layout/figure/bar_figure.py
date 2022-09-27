"""
   Descp: This class is used to represent a bar plot.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import Dict
import plotly.graph_objs as go

from dao_analyzer.web.apps.common.presentation.charts.layout.figure.figure import Figure
import dao_analyzer.web.apps.common.resources.colors as Color

class BarFigure(Figure):

    def __init__(self) -> None:
        super().__init__()
        super().configuration.add_x_params(params={'tickangle': True})
        super().configuration.add_y_params(params={'grid': True})


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
                marker_color=plot_data['color'],
        )

        super().configuration.add_x_params(
            params={
                # 'tickvals': plot_data['x'],
                'type': plot_data['type'],
                'tickformat': plot_data['x_format'],
            })

        super().configuration.disable_legend()

        layout: go.Layout = go.Layout(
            xaxis=super().configuration.get_x_axis_layout(),
            yaxis=super().configuration.get_y_axis_layout(),
            legend=super().configuration.get_legend(),
            shapes=super().configuration.get_shapes(),
            margin=self.configuration.get_margin(),
        )

        return {'data': [bar], 'layout': layout}
