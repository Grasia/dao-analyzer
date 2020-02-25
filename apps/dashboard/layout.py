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
    return html.Div(
        children = [
            html.Div(
                children = [
                    __generate_header(),
                ],
                className = 'main-header'
            ),

            html.Div(
                children = [
                    __generate_dao_selector(labels),
                    __generate_graphs(),
                ],
                className = 'main-body'
            ),

            html.Div(
                children = [],
                className = 'main-foot'
            ),
        ],
        className = 'main-root',
    )


def __generate_header() -> html.H2:
    return html.H1(TEXT['app_title'])
    

def __generate_dao_selector(labels: List[Dict[str, str]]) -> html.Div:
    return html.Div( 
        children = [
            html.Span(TEXT['dao_selector_title']),
            dcc.Dropdown(
                id = 'dao-dropdown',
                options = labels,
                className = 'drop-down'
            )
        ],
        className = 'pane dao-selector-pane',
    )


def __generate_graphs() -> html.Div:
    return html.Div(
        children = [
            __generate_new_users_graph(),
        ],
        className = 'graphs-container',
    )


def __generate_new_users_graph() -> html.Div:
    return html.Div(
        children = [
            html.H3(TEXT['new_users_title']),
            dcc.Graph(
                id = 'new-users-graph',
                figure = generate_bar_chart()
            ),
        ],
        className = 'pane graph-pane',
    )


def generate_bar_chart(data: Dict[str, List] = dict()) -> Dict:
    return {
        'data': [{
            'x': data['x'] if 'x' in data else [], 
            'y': data['y'] if 'y' in data else [], 
            'type': 'bar',
        }],
        'layout': {
            'xaxis': {
                #'range': [data['x'][0], data['x'][-1]],
                'ticks':'outside',
                'tick0': 0,
                'ticklen': 8,
                'tickwidth': 2
                },
        }
    }