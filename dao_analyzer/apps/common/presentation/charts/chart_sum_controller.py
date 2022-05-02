"""
   Descp: Controller class for charts that also modify the summary info

   Created on: 29-apr-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from dash.dependencies import Input, Output

from dao_analyzer.apps.common.business.i_metric_adapter import IMetricAdapter
from dao_analyzer.apps.common.presentation.charts.layout.chart_pane_layout import ChartPaneLayout
from dao_analyzer.apps.common.presentation.dashboard_view.dashboard_view import _get_dp_icon
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

        @app.callback(
            Output(self._css_id, 'children'),
            Output(self._number_css_id, 'children'),
            Output(self._evolution_css_id, 'children'),
            Input('org-dropdown', 'value'),
        )
        def update_chart(org_id):
            if not org_id:
                return self._layout.fill_child(None), '', ''
            
            data = self._adapter.get_plot_data(org_id)

            number = None
            if 'last_value' in data:
                number = data['last_value']
            elif 'total' in data:
                number = data['total']

            evolution = None
            if 'diff' in data:
                diffStr = f'{data["diff"]:.0f}'
                evolution = [_get_dp_icon(diffStr), " ", diffStr]

            return self._layout.fill_child(data), number, evolution
