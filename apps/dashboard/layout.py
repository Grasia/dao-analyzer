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

DARK_BLUE = '#2471a3'
LIGHT_BLUE = '#d4e6f1'

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
                    __generate_all_graphs(),
                ],
                className = 'main-body'
            ),

            html.Div(
                children = [],
                className = 'main-foot'
            ),
        ],
        className = 'root',
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


def __generate_all_graphs() -> html.Div:
    return html.Div(
        children = [
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'new-users',
                title = TEXT['new_users_title'],
                amount = TEXT['default_amount'],
                subtitle = TEXT['no_data'],
            ),
        ],
        className = 'graphs-container',
    )


def __generate_graph(figure_gen, css_id: str, title: str, amount: int, 
    subtitle: str) -> html.Div:

    return html.Div(
        children = [
            html.H3(title),
            html.H2(amount, id = f'{css_id}-amount'),
            html.Span(subtitle, id = f'{css_id}-subtitle'),
            dcc.Graph(
                id = f'{css_id}-graph',
                figure = figure_gen()
            ),
        ],
        className = 'pane graph-pane',
    )


def generate_bar_chart(x: List = [], y: List[int] = []) -> Dict:
    color = LIGHT_BLUE
    if x:
        color = [LIGHT_BLUE] * len(x)
        color[-1] = DARK_BLUE

    return {
        'data': [{
            'x': x,
            'y': y,
            'type': 'bar',
            'marker': { 'color': color }
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