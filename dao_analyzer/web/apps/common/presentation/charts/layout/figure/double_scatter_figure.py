"""
   Descp: This class is used to represent a double scatter figure
          with two sub-figures, one up, the other is below.

   Created on: 14-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import Dict
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from dao_analyzer.web.apps.common.presentation.charts.layout.figure.figure import Figure
import dao_analyzer.web.apps.common.resources.colors as Color

class DoubleScatterFigure(Figure):

    def __init__(self) -> None:
        super().__init__()
        super().configuration.add_axis(x_axis=2, y_axis=2)
        super().configuration.add_x_params(params={'removemarkers': True}, axis=0)
        super().configuration.add_x_params(params={'tickangle': True}, axis=1)
        super().configuration.add_y_params(params={'reverse_range': True}, axis=1)


    @staticmethod
    def get_empty_plot_data() -> Dict:
        return {
            'common': {
                    'x': list(),
                    'type': '-',
                    'x_format': '',
                    'ordered_keys': [],
                    'y_suffix': ''
        }}


    def get_empty_figure(self) -> Dict:
        return self.get_figure(plot_data = self.get_empty_plot_data())


    def get_figure(self, plot_data: Dict):
        """
        Returns the double scatter chart filled with plot_data.
        Arguments:
            * plot_data = {
                'type_i': { Each scatter type needs an entry in this dict and
                            to be registered in plot_data['common']['ordered_keys'].

                    'x': A list of x-axis values.
                    'y': A list filled with y-axis values.
                    'name': Bar type name.
                    'color': The bar's color.
                    'marker_symbol': Scatter symbol.
                    'position': 'up' or 'down' means the sub-figure to load them.
                }
                'common': { Common values for all the bars
                    'x': A list type filled with values.
                    'type': The type of the x-axis values, e.g. date.
                    'x_format': Format of the x-axis values, e.g. '%b, %Y'.
                    'ordered_keys': An ordered list of the dict-keys of each
                                    bar type. It's used to plot each bar type
                                    in a specific order.
                    'y_suffix': Suffix for the y-axis values.
                }
            } 
        """
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0)

        for k in plot_data['common']['ordered_keys']:
            fig.add_trace(
                go.Scatter(
                    x=plot_data[k]['x'], 
                    y=plot_data[k]['y'], 
                    marker=dict(
                        color=plot_data[k]['color'],
                        size=6,
                        opacity=0.5,
                        symbol=plot_data[k]['marker_symbol'],
                        line=dict(
                            width=1.2,
                            color=Color.BLACK,
                        )),
                    mode="markers",
                    name=plot_data[k]['name']
                ),
                row=1 if plot_data[k]['position'] == 'up' else 2,
                col=1)

        super().configuration.add_horizontal_line(y=0, y_ref='y')
        super().configuration.add_horizontal_line(y=0, y_ref='y2')
        super().configuration.enable_legend()

        super().configuration.add_x_params(
            params={
                # 'tickvals': plot_data['common']['x'],
                'type': plot_data['common']['type'],
                'tickformat': plot_data['common']['x_format'],
            },
            axis=1)

        super().configuration.add_y_params(
            params={
                'suffix': plot_data['common']['y_suffix'],
                #'matches': 'y2',
            },
            axis=0)

        super().configuration.add_y_params(
            params={
                'suffix': plot_data['common']['y_suffix'],
                #'matches': 'y2',
            },
            axis=1)

        fig.update_layout(
            xaxis=super().configuration.get_x_axis_layout(axis=0),
            xaxis2=super().configuration.get_x_axis_layout(axis=1),
            yaxis=super().configuration.get_y_axis_layout(axis=0),
            yaxis2=super().configuration.get_y_axis_layout(axis=1),
            legend=super().configuration.get_legend(),
            shapes=super().configuration.get_shapes(),
            plot_bgcolor=Color.WHITE
        )

        return fig
