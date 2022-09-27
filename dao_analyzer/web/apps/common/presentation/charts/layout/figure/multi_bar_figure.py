"""
   Descp: This class is used to represent a multiple bar figure, this means,
        stacked multibar-bar figure, and grouped multi-bar figure.

   Created on: 14-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import Dict, List
import plotly.graph_objs as go

from dao_analyzer.web.apps.common.presentation.charts.layout.figure.figure import Figure

class MultiBarFigure(Figure):
    STACK: int = 0
    GROUP: int = 1
    __TYPE_STACK: str = 'stack'
    __TYPE_GROUP: str = 'group'


    def __init__(self, bar_type: int) -> None:
        super().__init__()
        super().configuration.add_x_params(params={'tickangle': True})
        super().configuration.add_y_params(params={'grid': True})
        self.__bar_type: str = self.__get_type(bar_type)


    def __get_type(self, bar_type: int) -> str:
        btype: str = self.__TYPE_GROUP

        if bar_type == MultiBarFigure.STACK:
            btype = self.__TYPE_STACK

        return btype


    @staticmethod
    def get_empty_plot_data() -> Dict:
        return {
            'common': {
                'x': list(),
                'type': '-',
                'x_format': '', 
                'ordered_keys': []
            }
        }


    def get_empty_figure(self) -> Dict:
        return self.get_figure(plot_data = self.get_empty_plot_data())


    def get_figure(self, plot_data: Dict) -> Dict:
        """
        Returns the multi-bar chart filled with plot_data.
        Arguments:
            * plot_data = {
                'type_i': { Each bar type needs an entry in this dict and
                            to be registered in plot_data['common']['ordered_keys']

                    'y': A list filled with y-axis values.
                    'name': Bar type name.
                    'color': The bar's color.
                }
                'common': { Common values for all the bars
                    'x': A list type filled with values.
                    'type': The type of the x-axis values, e.g. date.
                    'x_format': Format of the x-axis values, e.g. '%b, %Y'.
                    'ordered_keys': An ordered list of the dict-keys of each
                                    bar type. It's used to plot each bar type
                                    in a specific order.
                }
            } 
        """
        bars: List = list()
        for k in plot_data['common']['ordered_keys']:
            bars.append(go.Bar(
                    x=plot_data['common']['x'], 
                    y=plot_data[k]['y'], 
                    name=plot_data[k]['name'], 
                    marker_color=plot_data[k]['color']))

        super().configuration.add_x_params(
            params={
                # 'tickvals': plot_data['common']['x'],
                'type': plot_data['common']['type'],
                'tickformat': plot_data['common']['x_format'],
            })

        super().configuration.enable_legend()

        layout: go.Layout = go.Layout(
            barmode=self.__bar_type,
            xaxis=super().configuration.get_x_axis_layout(),
            yaxis=super().configuration.get_y_axis_layout(),
            legend=super().configuration.get_legend(),
            shapes=super().configuration.get_shapes(),
            margin=self.configuration.get_margin(),
        )

        return {'data': bars, 'layout': layout}
