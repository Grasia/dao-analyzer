"""
   Descp: Controller class for charts that also modify the summary info

   Created on: 29-apr-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from datetime import date

from dash.dependencies import Input, Output

from dao_analyzer.apps.common.presentation.dashboard_view.dashboard_view import _gen_sum_hdr
from dao_analyzer.apps.common.business.i_metric_adapter import IMetricAdapter
from dao_analyzer.apps.common.presentation.charts.layout.chart_pane_layout import ChartPaneLayout
from .chart_controller import ChartController

class ChartHeaderController(ChartController):
    def __init__(self, 
        css_id: str, 
        layout: ChartPaneLayout, 
        adapter: IMetricAdapter,
        hdr_id: str,
    ):
        super().__init__(css_id, layout, adapter)
        self._hdr_id = hdr_id

    def bind_callback(self, app) -> None:

        @app.callback(
            Output(self._css_id, 'children'),
            Output(self._hdr_id, 'children'),
            Input('org-dropdown', 'value'),
        )
        def update_chart(org_id):
            if not org_id:
                return self._layout.fill_child(), _gen_sum_hdr()
            
            data = self._adapter.get_plot_data(org_id)

            # Get the first element with y greater than 0
            lastAct = next( (x for x,y in zip(reversed(data['x']), reversed(data['y'])) if y > 0), date.min)

            return self._layout.fill_child(data), _gen_sum_hdr(lastAct)
