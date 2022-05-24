"""
   Descp: Controller class for charts that also modify the summary info

   Created on: 29-apr-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from dash.dependencies import Input, Output, State

from dao_analyzer.apps.common.business.i_metric_adapter import IMetricAdapter
from dao_analyzer.apps.common.business.transfers.organization import OrganizationList
from dao_analyzer.apps.common.presentation.data_point_layout import DataPointLayout
from dao_analyzer.apps.common.presentation.charts.layout.chart_pane_layout import ChartPaneLayout
from .chart_controller import ChartController

class ChartSummaryController(ChartController):
    def __init__(self, 
        css_id: str, 
        layout: ChartPaneLayout, 
        adapter: IMetricAdapter,
        datapoint_layout: DataPointLayout,
    ):
        super().__init__(css_id, layout, adapter)
        self._dp_layout = datapoint_layout

    @property
    def _dp_id(self) -> str:
        return self._dp_layout._id

    @property
    def _number_css_id(self) -> str:
        return f'{self._dp_id}-number'

    @property
    def _evolution_css_id(self) -> str:
        return f'{self._dp_id}-evolution'

    def bind_callback(self, app) -> None:

        @app.callback(
            Output(self._css_id, 'children'),
            Output(self._dp_id, 'children'),
            Input('org-dropdown', 'value'),
            State('org-dropdown', 'options'),
        )
        def update_chart(org_id, org_options):
            if not org_id:
                return self._layout.fill_child(), self._dp_layout.fill_child()
            
            data = self._adapter.get_plot_data(org_id, OrganizationList.from_dict_representation(org_options))

            number = None
            if 'last_value' in data:
                number = data['last_value']
            elif 'total' in data:
                number = data['total']

            evolution = None
            # TODO: Add difference in absolute (modify basic_adapter.py)
            if 'diff' in data:
                evolution = f'{data["diff"]:.2f}%'

            return self._layout.fill_child(data), self._dp_layout.fill_child(number, evolution)
