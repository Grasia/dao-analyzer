"""
   layout.py

   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import dash_core_components as dcc
import dash_html_components as html

from apps.dashboard.en_strings import TEXT


def generate_layout(labels: list) -> html.Div:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of labels to fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    return html.Div(children=[
        __generate_header(),
        __generate_dao_selector(labels),
    ])


def __generate_header() -> html.H2:
    return html.H2(TEXT['app_title'])


def __generate_dao_selector(labels: list) -> html.Div:
    return html.Div( children=[
            html.Span(TEXT['dao_selector_title']),
            dcc.Dropdown(
                id='dao-dropdown',
                options=[ {'label': lb, 'value': lb} for lb in labels ]
            )
        ]
    )