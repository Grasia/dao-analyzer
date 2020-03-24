"""
   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from src.apps.daostack.resources.strings import TEXT

DARK_BLUE = '#2471a3'
LIGHT_BLUE = '#d4e6f1'
DARK_RED = '#F44336'
LIGHT_RED = '#EF9A9A'
DARK_GREEN = '#4CAF50'
LIGHT_GREEN = '#A5D6A7'

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
                id = 'org-dropdown',
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
                subtitle = TEXT['no_data_selected'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'different-voters',
                title = TEXT['different_voters_title'],
                amount = TEXT['default_amount'],
                subtitle = TEXT['no_data_selected'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'total-votes',
                title = TEXT['total_votes_title'],
                amount = TEXT['default_amount'],
                subtitle = TEXT['no_data_selected'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'different-stakers',
                title = TEXT['different_stakers_title'],
                amount = TEXT['default_amount'],
                subtitle = TEXT['no_data_selected'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'total-stakes',
                title = TEXT['total_stakes_title'],
                amount = TEXT['default_amount'],
                subtitle = TEXT['no_data_selected'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'new-proposal',
                title = TEXT['new_proposals_title'],
                amount = TEXT['default_amount'],
                subtitle = TEXT['no_data_selected'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'proposal-boost-outcome',
                title = TEXT['proposal_boost_outcome_title'],
            ),
            __generate_graph(
                figure_gen = generate_double_dot_chart,
                css_id = 'proposal-outc-majority',
                title = TEXT['proposal_outcome_majority_title'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'proposal-boost-succ-ratio',
                title = TEXT['proposal_boost_succ_ratio_title'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'proposal-total-succ-ratio',
                title = TEXT['proposal_total_succ_ratio_title'],
            ),
        ],
        className = 'graphs-container',
    )


def __generate_graph(figure_gen, css_id: str, title: str, amount: str = None,
subtitle: str = None) -> html.Div:

    children: List = [html.H3(title)]
    if amount:
        children.append(html.H2(amount, id = f'{css_id}-amount'))
    if subtitle:
        children.append(html.Span(subtitle, id = f'{css_id}-subtitle'))

    children.append(dcc.Graph(id = f'{css_id}-graph', figure = figure_gen()))

    return html.Div(children = children, className = 'pane graph-pane')


def generate_bar_chart(data: Dict = None, barmode: str = 'group') -> Dict:
    if not data:
        data = {'common': {'x': list(), 'type': '-', 'x_format': '', 
            'ordered_keys': []}}

    bars: List = list()
    for k in data['common']['ordered_keys']:
        bars.append(go.Bar(
                x=data['common']['x'], 
                y=data[k]['y'], 
                name=data[k]['name'], 
                marker_color=data[k]['color']))

    layout: go.Layout = go.Layout(
        barmode=barmode,
        xaxis=__get_axis_layout(
            tickvals=data['common']['x'], 
            l_type=data['common']['type'], 
            tickformat=data['common']['x_format']),
        yaxis=__get_axis_layout(tickangle=False),
        legend=__get_legend())

    return {'data': bars, 'layout': layout}


def generate_double_dot_chart(data: Dict = None) -> Dict:
    if not data:
        data = {'common': {'x': list(), 'type': '-', 'x_format': '',
            'ordered_keys': [], 'y_suffix': ''}}

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0)

    for k in data['common']['ordered_keys']:
        fig.add_trace(
            go.Scatter(
                x=data[k]['x'], 
                y=data[k]['y'], 
                marker=dict(color=data[k]['color'], size=12),
                mode="markers",
                name=data[k]['name']),
            row=1 if data[k]['position'] == 'up' else 2,
            col=1)

    fig.update_layout(
        xaxis2=__get_axis_layout(
            tickvals=data['common']['x'], 
            l_type=data['common']['type'], 
            tickformat=data['common']['x_format'],
        ),
        yaxis=__get_axis_layout(
            suffix=data['common']['y_suffix'],
            tickangle=False,
        ),
        yaxis2=__get_axis_layout(
            reverse_range=True,
            suffix=data['common']['y_suffix'],
            tickangle=False,
        ),
        legend=__get_legend(),
        plot_bgcolor="white")

    return fig


def __get_axis_layout(tickvals: List = None, l_type: str = '-', 
l_range: list = None, reverse_range: bool = False, grid: bool = False,
suffix: str = '', tickformat: str = '', tickangle: bool = True) -> Dict:

    axis_l: Dict[str, str] = {
        'type': l_type,
        'ticks': 'outside',
        'tick0': 0,
        'ticklen': 5,
        'tickwidth': 2,
        'ticksuffix': suffix,
        'showline': True, 
        'linewidth': 2, 
        'linecolor': 'black',
        'showgrid': grid,
        'gridwidth': 1,
        'gridcolor': 'LightPink',
    }

    if tickvals:
        axis_l['tickvals'] = tickvals
    if reverse_range:
        axis_l['autorange'] = 'reversed'
    if l_range:
        axis_l['range'] = l_range
    if tickformat:
        axis_l['tickformat'] = tickformat
    if tickangle:
        axis_l['tickangle'] = 45

    return axis_l


def __get_legend() -> Dict:
    return {'orientation': 'h', 'x': 0, 'y': -0.3}