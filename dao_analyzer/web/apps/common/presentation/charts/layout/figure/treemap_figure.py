"""
   Descp: This class is used to represent a treemap

   Created on: 10-mar-2022

   Copyright 2020-2022 David Davó
        <ddavo@ucm.es>
"""
from typing import Dict
import plotly.graph_objects as go

from . import Figure

class TreemapFigure(Figure):
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def get_empty_plot_data() -> Dict:
        return {
            'ids': [],
            'labels': [],
            'parents': [],
            'values': []
        }
    
    def get_empty_figure(self) -> Dict:
        return self.get_figure(plot_data=self.get_empty_plot_data())
    
    def get_figure(self, plot_data: Dict) -> Dict:
        """
        Returns the treemap filled with plot_data
        Arguments:
            * plot_data: see https://plotly.com/python/reference/treemap/
        """
        # TODO: Instead of popping 'total', pass only needed values

        plot_data.pop('total', None)
        treemap: go.Treemap = go.Treemap(**plot_data)
        layout: go.Layout = go.Layout(
            margin=self.configuration.get_margin(),
        )

        return {'data': [treemap], 'layout': layout}
