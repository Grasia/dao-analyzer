"""
   Descp: Controller class for all the charts.

   Created on: 10-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from dash.dependencies import Input, Output

from src.app import app
from src.apps.daostack.presentation.charts.chart_pane_layout \
import ChartPaneLayout

class ChartController():

    def __init__(self, css_id: str, layout: ChartPaneLayout, metric: Metric) -> None:
        self.__layout = layout
        self.__metric = metric

        self.bind_callback(
            app = app, 
            chart = css_id,
            elem1 = f'{css_id}{ChartPaneLayout.SUFFIX_ID_SUBTITLE1}',
            elem2 = f'{css_id}{ChartPaneLayout.SUFFIX_ID_SUBTITLE2}',
            input_callback = 'org-dropdown')


    def bind_callback(self, app, chart, elem1, elem2, input_callback) -> None:

        @app.callback(
            [Output(chart, 'figure'),
             Output(elem1, 'children'),
             Output(elem2, 'children')],
            [Input(input_callback, 'value')]
        )
        def update_chart(org_id):
            if not org_id:
                self.__layout.get_layout()
        # TODO
            
