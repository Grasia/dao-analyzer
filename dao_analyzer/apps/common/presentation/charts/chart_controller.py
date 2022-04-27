"""
   Descp: Controller class for all the charts.

   Created on: 10-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from dash.dependencies import Input, Output

from dao_analyzer.apps.common.presentation.charts.layout.chart_pane_layout \
    import ChartPaneLayout
from dao_analyzer.apps.common.business.i_metric_adapter import IMetricAdapter

class ChartController():

    def __init__(self, css_id: str, layout: ChartPaneLayout, adapter: IMetricAdapter) -> None:
        self.__layout: ChartPaneLayout = layout
        self.__adapter: IMetricAdapter = adapter
        self.__css_id: str = css_id


    @property
    def layout(self) -> ChartPaneLayout:
        return self.__layout


    def bind_callback(self, app) -> None:

        @app.callback(
             Output(self.__css_id, 'children'),
            [Input('org-dropdown', 'value')]
        )
        def update_chart(org_id):
            if not org_id:
                self.__layout.get_layout()

            data = self.__adapter.get_plot_data(org_id)
            return self.__layout.fill_child(plot_data=data)
