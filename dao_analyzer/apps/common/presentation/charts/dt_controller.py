"""
   Descp: Controller class for the DataTables

   Created on: 16-mar-2022

   Copyright 2020-2022 David Davó Laviña
        <ddavo@ucm.es>
"""

from dash.dependencies import Input, Output

from dao_analyzer.apps.common.business.transfers.tabular_data import TabularData

from .layout import DataTableLayout
from ...business.i_metric_adapter import IMetricAdapter

class DataTableController():
    def __init__(self, table_id: str, layout: DataTableLayout, adapter: IMetricAdapter):
        self.__css_id: str = table_id
        self.__layout: DataTableLayout = layout
        self.__adapter: IMetricAdapter = adapter
    
    @property
    def layout(self) -> DataTableLayout:
        return self.__layout
    
    def bind_callback(self, app) -> None:
        @app.callback(
            [Output(self.__css_id, 'data'), Output(self.__css_id, 'columns')],
            [Input('org-dropdown', 'value')]
        )
        def update_table(org_id):
            if not org_id:
                self.__layout.get_layout()

            td: TabularData = self.__adapter.get_plot_data(org_id)
            return td.data, td.columns