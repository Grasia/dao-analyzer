"""
   Descp: It's used to manage the dashboard events.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
from dash.dependencies import Input, Output

from src.app import app
import src.apps.daostack.presentation.layout as ly
from src.apps.daostack.resources.strings import TEXT
from src.apps.daostack.business.app_service import get_service


def init():
    pass


def __get_data_from_metric(metric: Dict) -> List:
    return [
        ly.generate_bar_chart(metric),
        TEXT['graph_amount'].format(
            metric['common']['last_serie_elem'], 
            metric['common']['last_value']),
        TEXT['graph_subtitle'].format(metric['common']['diff'])
    ]


def __get_empty_chart(chart) -> List:
    return [
        chart,
        TEXT['default_amount'],
        TEXT['no_data_selected']
    ]


@app.callback(
    [Output('new-users-graph', 'figure'),
    Output('new-users-subtitle1', 'children'),
    Output('new-users-subtitle2', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_new_user_graph(org_id):
    if not org_id:
        return __get_empty_chart(chart=ly.generate_bar_chart())
    
    return __get_data_from_metric(get_service().get_metric_new_users(org_id))


@app.callback(
    [Output('active-users-graph', 'figure'),
    Output('active-users-subtitle1', 'children'),
    Output('active-users-subtitle2', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_active_user_graph(org_id):
    if not org_id:
        return __get_empty_chart(chart=ly.generate_bar_chart())
    
    return __get_data_from_metric(get_service().get_metric_active_users(org_id))


@app.callback(
    [Output('different-voters-graph', 'figure'),
    Output('different-voters-subtitle1', 'children'),
    Output('different-voters-subtitle2', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_different_voters_graph(org_id):
    if not org_id:
        return __get_empty_chart(chart=ly.generate_bar_chart())
    
    return __get_data_from_metric(get_service().
        get_metric_different_voters(org_id))


@app.callback(
    [Output('different-stakers-graph', 'figure'),
    Output('different-stakers-subtitle1', 'children'),
    Output('different-stakers-subtitle2', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_different_stakers_graph(org_id):
    if not org_id:
        return __get_empty_chart(chart=ly.generate_bar_chart())
    
    return __get_data_from_metric(get_service().
        get_metric_different_stakers(org_id))


@app.callback(
    [Output('new-proposal-graph', 'figure'),
    Output('new-proposal-subtitle1', 'children'),
    Output('new-proposal-subtitle2', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_new_proposal_graph(org_id):
    if not org_id:
        return __get_empty_chart(chart=ly.generate_bar_chart())

    return __get_data_from_metric(get_service().get_metric_new_proposals(org_id))


# @app.callback(
#     [Output('total-votes-graph', 'figure'),
#     Output('total-votes-subtitle1', 'children'),
#     Output('total-votes-subtitle2', 'children')],
#     [Input('org-dropdown', 'value')]
# )
# def update_total_votes_graph(org_id):
#     if not org_id:
#         return __get_empty_chart(chart=ly.generate_bar_chart())

#     return __get_data_from_metric(get_service().get_metric_total_votes(org_id))


@app.callback(
    [Output('total-stakes-graph', 'figure'),
    Output('total-stakes-subtitle1', 'children'),
    Output('total-stakes-subtitle2', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_total_stakes_graph(org_id):
    if not org_id:
        return __get_empty_chart(chart=ly.generate_bar_chart())

    return __get_data_from_metric(get_service().get_metric_total_stakes(org_id))


@app.callback(
    Output('proposal-outc-majority-graph', 'figure'),
    [Input('org-dropdown', 'value')]
)
def update_proposal_majority_graph(org_id):
    if not org_id:
        return ly.generate_bar_chart()

    data: Dict = get_service().get_metric_proposal_majority(org_id)

    return ly.generate_double_dot_chart(data=data)


@app.callback(
    Output('proposal-boost-outcome-graph', 'figure'),
    [Input('org-dropdown', 'value')]
)
def update_proposal_boost_outcome_graph(org_id):
    if not org_id:
        return ly.generate_bar_chart()

    metric: Dict = get_service().get_metric_proposal_boost_outcome(org_id)
    return ly.generate_bar_chart(data=metric, barmode='stack')


@app.callback(
    Output('proposal-total-succ-ratio-graph', 'figure'),
    [Input('org-dropdown', 'value')]
)
def update_proposal_total_succ_ratio(org_id):
    if not org_id:
        return ly.generate_bar_chart()

    metric = get_service().get_metric_prop_total_succes_ratio(org_id)
    return ly.generate_bar_chart(data=metric)


@app.callback(
    Output('proposal-boost-succ-ratio-graph', 'figure'),
    [Input('org-dropdown', 'value')]
)
def update_proposal_boost_succ_ratio(org_id):
    if not org_id:
        return ly.generate_bar_chart()

    metric = get_service().get_metric_prop_boost_succes_ratio(org_id)
    return ly.generate_bar_chart(metric)


@app.callback(
    [Output('total-votes-option-graph', 'figure'),
    Output('total-votes-option-subtitle1', 'children'),
    Output('total-votes-option-subtitle2', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_total_votes_option_graph(org_id):
    if not org_id:
        return __get_empty_chart(chart=ly.generate_bar_chart())

    metric: Dict = get_service().get_metric_total_votes_option(org_id)
    return [
        ly.generate_bar_chart(data=metric, barmode='stack'),
        TEXT['graph_amount'].format(
            metric['common']['last_serie_elem'], 
            metric['common']['last_value']),
        TEXT['graph_subtitle'].format(metric['common']['diff'])
        ]


# @app.callback(
#     Output('total-stakes-option-graph', 'figure'),
#     [Input('org-dropdown', 'value')]
# )
# def update_total_stakes_option_graph(org_id):
#     if not org_id:
#         return __get_empty_chart(chart=ly.generate_bar_chart())

#     metric: Dict = get_service().get_metric_total_stakes_option(org_id)
#     return ly.generate_bar_chart(data=metric, barmode='stack')
