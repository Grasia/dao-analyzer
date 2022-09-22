"""
   Descp: Controller class for charts that also modify the summary info

   Created on: 29-apr-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from dash.dependencies import Input, Output, State
import numpy as np

from dao_analyzer.web.apps.common.business.i_metric_adapter import IMetricAdapter
from dao_analyzer.web.apps.common.business.transfers.organization import OrganizationList
from dao_analyzer.web.apps.common.presentation.charts.layout.chart_pane_layout import ChartPaneLayout
from .chart_controller import ChartController

class ChartSummaryController(ChartController):
    def __init__(self, 
        css_id: str, 
        layout: ChartPaneLayout, 
        adapter: IMetricAdapter,
        dp_id: str,
    ):
        super().__init__(css_id, layout, adapter)
        self._dp_id = dp_id

    def bind_callback(self, app) -> None:
        @app.callback(
            Output(self._css_id, 'children'),
            Output(self._dp_id, 'number'),
            Output(self._dp_id, 'evolution'),
            Output(self._dp_id, 'evolution_rel'),
            Input('org-dropdown', 'value'),
            State('org-dropdown', 'options'),
        )
        def update_chart(org_id, org_options):
            if not org_id:
                return self._layout.fill_child(), np.NaN, np.NaN, np.NaN
            
            data = self._adapter.get_plot_data(org_id, OrganizationList.from_dict_representation(org_options))

            number = None
            if 'last_value' in data:
                number = data['last_value']
            elif 'total' in data:
                number = data['total']

            evolution = data.get('diff', None)
            evolution_rel = data.get('diff_rel', None)

            return self._layout.fill_child(data), number, evolution, evolution_rel
