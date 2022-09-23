"""
   Descp: This class is used to represent a calendar plot.

   Created on: 21-apr-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from typing import Dict

import plotly.graph_objs as go
from plotly_calplot import month_calplot

from .figure import Figure
import dao_analyzer.web.apps.common.resources.colors as Color

class CalFigure(Figure):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_empty_plot_data() -> Dict:
        return {
            'x': [],
            'y': [],
        }
    
    def get_empty_figure(self) -> Dict:
        return self.get_figure(self.get_empty_plot_data())
    
    def get_figure(self, plot_data: Dict) -> Dict:
        fig: go.Figure = month_calplot(
            x=plot_data['x'],
            y=plot_data['y'],
            gap=3,
            year_height=50,
        )

        fig.update_layout(
            margin=self.configuration.get_margin(),
            xaxis = {
                'tickfont_color': Color.TICKFONT_COLOR,
            },
            yaxis = {
                'tickfont_color': Color.TICKFONT_COLOR,
            }
        )

        return fig