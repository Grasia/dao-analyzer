"""
   Descp: Common pane which wraps data table and other components.

   Created on: 15-mar-2022

   Copyright 2020-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from dash import html, dcc
from dash.dash_table import DataTable

from . import ILayout
from .data_table_configuration import DataTableConfiguration

class DataTableLayout(ILayout):
    SUFFIX_ID_TABLE: str = '-dtable'
    
    def __init__(self, title: str, css_id: str) -> None:
        self.__title: str = title
        self.__css_id: str = css_id
        self.__configuration: DataTableConfiguration = DataTableConfiguration()
    
    @property
    def table_id(self):
        return f'{self.__css_id}{self.SUFFIX_ID_TABLE}'

    @property
    def configuration(self) -> DataTableConfiguration:
        return self.__configuration

    def get_layout(self) -> html.Div:
        children = [
            html.Div(children=[
                html.Span(
                    self.__title,
                    className='graph-pane-title'
                ),
                html.Span('nothing', className='hide'),
            ], className='d-flex flex-column chart-header'),
            DataTable(
                id=self.table_id,
                # style_table={'height': '450px', 'margin-top': '40px', 'overflowY': 'auto'},
                sort_action='native',
                page_size=14
            )
        ]

        return html.Div(
            children=dcc.Loading(
                type="circle",
                color=self.configuration.color,
                children=html.Div(
                    children=children,
                    id=self.__css_id,
                    className='d-flex flex-column'
                ),
                className='dcc-loading',
                parent_style={'flex': '1 1 auto'},
                style={'flex': '1 1 auto'}
            ),
            className=f'pane {self.configuration.css_border} col',
            style={'align-self': 'stretch', 'display': 'flex'}
        )