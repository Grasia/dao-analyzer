"""
   Descp: Controller class for charts that also modify the summary info

   Created on: 29-apr-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from dash.dependencies import Input, Output

from dao_analyzer.apps.common.business.i_metric_adapter import IMetricAdapter
from dao_analyzer.apps.common.presentation.charts.layout.chart_pane_layout import ChartPaneLayout
from dao_analyzer.apps.common.presentation.dashboard_view.controller import _get_dp_icon
from .chart_controller import ChartController

class ChartSummaryController(ChartController):
    def __init__(self, 
        css_id: str, 
        layout: ChartPaneLayout, 
        adapter: IMetricAdapter,
        datapoint_id: str,
    ):
        super().__init__(css_id, layout, adapter)
        self._dp_id = datapoint_id

    @property
    def _number_css_id(self) -> str:
        return f'{self._dp_id}-number'

    @property
    def _evolution_css_id(self) -> str:
        return f'{self._dp_id}-evolution'

    def bind_callback(self, app) -> None:
        print("Number id:", self._number_css_id)

        @app.callback(
            Output(self._css_id, 'children'),
            Output(self._number_css_id, 'children'),
            Output(self._evolution_css_id, 'children'),
            Input('org-dropdown', 'value'),
        )
        def update_chart(org_id):
            print(f"Inside chart summary controller {self._css_id}. dp: {self._dp_id}")
            if not org_id:
                self._layout.get_layout(), ''
            
            data = self._adapter.get_plot_data(org_id)

            diffStr = f'{data["diff"]:.0f}'
            evolution = [_get_dp_icon(diffStr), " ", diffStr]
            return self._layout.fill_child(data), data['last_value'], evolution
