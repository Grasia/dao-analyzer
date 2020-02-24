"""
   layout.py

   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List
import dash_core_components as dcc
import dash_html_components as html

from apps.dashboard.strings import TEXT


def generate_layout(labels: List[Dict[str, str]]) -> html.Div:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    return html.Div(children=[
        __generate_header(),
        __generate_dao_selector(labels),
        __generate_new_users_graph(),
        html.Div(id='kk'),
    ])


def __generate_header() -> html.H2:
    return html.H2(TEXT['app_title'])


def __generate_dao_selector(labels: List[Dict[str, str]]) -> html.Div:
    return html.Div( children=[
            html.Span(TEXT['dao_selector_title']),
            dcc.Dropdown(
                id = 'dao-dropdown',
                options = labels
            )
        ]
    )


def __generate_new_users_graph() -> html.Div:
    return html.Div(children=[
        html.H4(TEXT['new_users_title']),
        dcc.Graph(
            id = 'new-users-graph',
            figure = {'data': [{'x': [], 'y': [], 'type': 'bar'}]}
        ),
    ])