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
import src.apps.daostack.resources.colors as Color


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
        children=[
            html.Div(
                children=[
                    __generate_header(),
                ],
                className='main-header fix-height'
            ),

            html.Div(
                children=[
                    __generate_dao_selector(labels),
                    __generate_user_charts(),
                    __generate_vote_charts(),
                    __generate_stake_charts(),
                    __generate_proposal_charts(),
                ],
                className='main-body'
            ),

            html.Div(
                children=[__generate_foot()],
                className='main-foot'
            ),
        ],
        className='root',
    )


def __generate_header() -> html.H1:
    return html.H1(TEXT['app_title'])
    

def __generate_dao_selector(labels: List[Dict[str, str]]) -> html.Div:
    return html.Div( 
        children = [
            html.Span(TEXT['dao_selector_title']),
            dcc.Dropdown(
                id='org-dropdown',
                options=labels,
                className='drop-down'
            )
        ],
        className='dao-selector-pane',
    )


def __generate_foot() -> html.Div:
    return html.Div(children=[
                    html.Div(children=[
                        html.Span(TEXT['github'], className='right-separator bold'),
                        html.A(TEXT['github_url'], href=TEXT['github_url'], target='_blank')
                    ], className='center-aligner medium-font small-vertical-margin'),
                    html.Div(children=[
                        html.Div(children=[
                            html.A(children=[
                                html.Img(src=TEXT['cc_image_url'], className='license-img'),
                            ], href=TEXT['cc_url'], target='_blank'),
                            html.A(TEXT['cc_license_text'], href=TEXT['cc_url'], target='_blank'),
                        ], className='column-container center-aligner'),
                        html.Div(children=[
                            html.A(children=[
                                html.Img(src=TEXT['gpl_image_url'], className='license-img'),
                            ], href=TEXT['gpl_url'], target='_blank'),
                            html.A(TEXT['gpl_license_text'], href=TEXT['gpl_url'], target='_blank'),
                        ], className='column-container center-aligner')
                    ], className='row-container space-aligner small-vertical-margin')
                ])


def __generate_user_charts() -> html.Div:
    return html.Div(
        children=[
            html.Div(TEXT['rep_holder_title'], className='title-section'),
            html.Div(children=[
                __generate_graph(
                    figure_gen=generate_bar_chart,
                    css_id='new-users',
                    title=TEXT['new_users_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                ),
                __generate_graph(
                    figure_gen=generate_bar_chart,
                    css_id='active-users',
                    title=TEXT['active_users_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                ),
            ],
            className='graph-section'),
        ],
        className='section',
    )


def __generate_vote_charts() -> html.Div:
    return html.Div(
        children=[
            html.Div(TEXT['vote_title'], className='title-section'),
            html.Div(children=[
                # __generate_graph(
                #     figure_gen = generate_bar_chart,
                #     css_id = 'total-votes',
                #     title = TEXT['total_votes_title'],
                #     amount = TEXT['default_amount'],
                #     subtitle = TEXT['no_data_selected'],
                # ),
                __generate_graph(
                    figure_gen=generate_bar_chart,
                    css_id='total-votes-option',
                    title=TEXT['total_votes_option_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                ),
                __generate_graph(
                    figure_gen = generate_bar_chart,
                    css_id='different-voters',
                    title=TEXT['different_voters_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                ),
            ],
            className='graph-section'),
        ],
        className='section',
    )


def __generate_stake_charts() -> html.Div:
    return html.Div(
        children=[
            html.Div(TEXT['stake_title'], className='title-section'),
            html.Div(children=[
                __generate_graph(
                    figure_gen = generate_bar_chart,
                    css_id='total-stakes',
                    title=TEXT['total_stakes_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                ),
                # __generate_graph(
                #     figure_gen = generate_bar_chart,
                #     css_id = 'total-stakes-option',
                #     title = TEXT['total_stakes_option_title'],
                # ),
                __generate_graph(
                    figure_gen=generate_bar_chart,
                    css_id='different-stakers',
                    title=TEXT['different_stakers_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                ),
            ],
            className='graph-section'),
        ],
        className='section',
    )


def __generate_proposal_charts() -> html.Div:
    return html.Div(
        children=[
            html.Div(TEXT['proposal_title'], className='title-section'),
            html.Div(children=[
                __generate_graph(
                    figure_gen=generate_bar_chart,
                    css_id='new-proposal',
                    title=TEXT['new_proposals_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                ),
                __generate_graph(
                    figure_gen=generate_double_dot_chart,
                    css_id='proposal-outc-majority',
                    title=TEXT['proposal_outcome_majority_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                    show_subsection=False,
                ),
                __generate_graph(
                    figure_gen=generate_bar_chart,
                    css_id='proposal-boost-outcome',
                    title=TEXT['proposal_boost_outcome_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                    show_subsection=False,
                ),
                __generate_graph(
                    figure_gen=generate_bar_chart,
                    css_id='proposal-total-succ-ratio',
                    title=TEXT['proposal_total_succ_rate_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                    show_subsection=False,
                ),
                __generate_graph(
                    figure_gen=generate_bar_chart,
                    css_id='proposal-boost-succ-ratio',
                    title=TEXT['proposal_boost_succ_rate_title'],
                    amount=TEXT['default_amount'],
                    subtitle=TEXT['no_data_selected'],
                    show_subsection=False,
                ),
            ],
            className='graph-section'),
        ],
        className='section')


def __generate_graph(figure_gen, css_id: str, title: str, amount: str,
subtitle: str, show_subsection: bool = True) -> html.Div:

    hide: str = '' if show_subsection else 'hide'

    children: List = [html.Span(title, className='graph-title1')]
    children.append(html.Span(
        amount, 
        id=f'{css_id}-amount', 
        className=f'graph-title2 {hide}'))
    children.append(html.Span(
        subtitle, 
        id=f'{css_id}-subtitle',
        className=hide))

    children.append(dcc.Loading(
        type="circle",
        color=Color.DARK_BLUE,
        children=dcc.Graph(id=f'{css_id}-graph', figure=figure_gen())))

    return html.Div(children=children, className='pane graph-pane')


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
        xaxis=__get_axis_layout(args={
            'tickvals': data['common']['x'], 
            'type': data['common']['type'], 
            'tickformat': data['common']['x_format'],
            'tickangle': True}
        ),
        yaxis=__get_axis_layout(args={'grid': True}),
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
                marker=dict(
                    color=data[k]['color'],
                    size=6,
                    opacity=0.5,
                    symbol=data[k]['marker_symbol'],
                    line=dict(
                        width=1.2,
                        color='black',
                    )),
                mode="markers",
                name=data[k]['name']),
            row=1 if data[k]['position'] == 'up' else 2,
            col=1)

    fig.update_layout(
        xaxis=__get_axis_layout(args={'removemarkers': True}),
        xaxis2=__get_axis_layout(args={
            'tickvals': data['common']['x'], 
            'type': data['common']['type'], 
            'tickformat': data['common']['x_format'],
            'tickangle': True}
        ),
        yaxis=__get_axis_layout(args={
            'suffix': data['common']['y_suffix'],
            #'matches': 'y2',
            }
        ),
        yaxis2=__get_axis_layout(args={
            'suffix': data['common']['y_suffix'],
            #'matches': 'y',
            'reverse_range': True,
            }
        ),
        shapes=[
            __get_horizontal_line(y=0.0, y_ref='y'), 
            __get_horizontal_line(y=0.0, y_ref='y2')],
        legend=__get_legend(),
        plot_bgcolor="white")

    return fig


def __get_horizontal_line(y, y_ref: str):
    return {
            'type': 'line',
            'xref': 'paper',
            'yref': y_ref,
            'x0': 0,
            'y0': y,
            'x1': 1,
            'y1': y,
            'line':{
                'color': 'black',
                'width': 0.5,
                'dash':'dot'
            }
        }


def __get_axis_layout(args: Dict) -> Dict:
    axis_l: Dict[str, str] = {
        'type': args['type'] if 'type' in args else '-',
        'ticks': 'outside',
        'ticklen': 5,
        'tickwidth': 2,
        'ticksuffix': args['suffix'] if 'suffix' in args else '',
        'showline': True, 
        'linewidth': 2, 
        'linecolor': 'black',
        'showgrid': args['grid'] if 'grid' in args else False,
        'gridwidth': 0.5,
        'gridcolor': '#B0BEC5',
    }

    if 'removemarkers' in args:
        axis_l['ticklen'] = 0
        axis_l['tickwidth'] = 0
    if 'tickvals' in args:
        axis_l['tickvals'] = args['tickvals']
    if 'reverse_range' in args:
        axis_l['autorange'] = 'reversed'
    if 'l_range' in args:
        axis_l['range'] = args['l_range']
    if 'tickformat' in args:
        axis_l['tickformat'] = args['tickformat']
    if 'tickangle' in args:
        axis_l['tickangle'] = 45
    if 'matches' in args:
        axis_l['matches'] = args['matches']

    return axis_l


def __get_legend() -> Dict:
    return {'orientation': 'h', 'x': 0, 'y': 1.2}
