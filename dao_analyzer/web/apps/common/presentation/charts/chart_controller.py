"""
   Descp: Controller class for all the charts.

   Created on: 10-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from dash.dependencies import Input, Output, State, MATCH
from dao_analyzer.web.apps.common.business.transfers.organization.organization_list import OrganizationList

from dao_analyzer.web.apps.common.presentation.charts.layout.chart_pane_layout \
    import ChartPaneLayout
from dao_analyzer.web.apps.common.business.i_metric_adapter import IMetricAdapter

class ChartController():

    def __init__(self, css_id: str, layout: ChartPaneLayout, adapter: IMetricAdapter) -> None:
        self._layout: ChartPaneLayout = layout
        self._adapter: IMetricAdapter = adapter
        self._css_id: str = css_id


    @property
    def layout(self) -> ChartPaneLayout:
        return self._layout


    def bind_callback(self, app) -> None:
        from dao_analyzer.web.app import background_callback_manager
        import inspect, traceback

        @app.callback(
            # Output({'_id': self._css_id}, 'children'),
            Output(self._css_id, 'children'),
            {
                'org_id': Input('org-dropdown', 'value'),
                'org_options': State('org-dropdown', 'options'),
                # '_id': State('_id': self._css_id}, 'id'),
                '_id': State(self._css_id, 'id'),
            },
            # background=True,
            # manager=background_callback_manager,
            # cache_args_to_ignore=['org_options'],
        )
        def update_chart(org_id, org_options, _id):
            if not org_id:
                self._layout.get_layout()

            data = self._adapter.get_plot_data(org_id, OrganizationList.from_dict_representation(org_options))
            return self._layout.fill_child(plot_data=data)

        print(f"Binding callback for {self._css_id}, f: {update_chart}, qname: {update_chart.__qualname__}")
