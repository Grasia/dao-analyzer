"""
   Descp: Controller class for all the charts.

   Created on: 10-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from dash.dependencies import Input, Output

from src.app import app
from src.apps.common.presentation.charts.layout.chart_pane_layout \
    import ChartPaneLayout
from src.apps.common.business.i_metric_adapter import IMetricAdapter

class ChartController():

    def __init__(self, css_id: str, layout: ChartPaneLayout, adapter: IMetricAdapter) -> None:
        self.__layout: ChartPaneLayout = layout
        self.__adapter: IMetricAdapter = adapter
        self.bind_callback(
            app=app, 
            pane=css_id,
            input_callback='org-dropdown')


    @property
    def layout(self) -> ChartPaneLayout:
        return self.__layout


    def bind_callback(self, app, pane, input_callback) -> None:

        @app.callback(
             Output(pane, 'children'),
            [Input(input_callback, 'value')]
        )
        def update_chart(org_id):
            if not org_id:
                self.__layout.get_layout()

            data = self.__adapter.get_plot_data(org_id)
            return self.__layout.fill_child(plot_data=data)
