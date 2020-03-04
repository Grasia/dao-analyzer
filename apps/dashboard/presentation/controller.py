"""
   Descp: It's used to manage the dashboard events.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app import app
import apps.dashboard.presentation.layout as ly
from apps.dashboard.resources.strings import TEXT
from apps.dashboard.business.transfers.stacked_serie import StackedSerie
import apps.dashboard.business.app_service as service


def init():
    # init controller
    pass


def __get_data_from_metric(metric: StackedSerie) -> List:
    i_stack: int = 0
    return [
        ly.generate_bar_chart(
            x = metric.get_serie(), 
            y = metric.get_i_stack(i_stack)),
        TEXT['graph_month_amount'].format(metric.get_last_serie_elem(), 
            metric.get_last_value(i_stack)),
        TEXT['graph_subtitle'].format(metric.get_diff_last_values(i_stack))
    ]


@app.callback(
    [Output('new-users-graph', 'figure'),
    Output('new-users-month-amount', 'children'),
    Output('new-users-subtitle', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_new_user_graph(org_id):
    if not org_id:
        raise PreventUpdate

    #service.get_metric_type_proposals(org_id)
    
    return __get_data_from_metric(service.get_metric_new_users(org_id))


@app.callback(
    [Output('new-proposal-graph', 'figure'),
    Output('new-proposal-month-amount', 'children'),
    Output('new-proposal-subtitle', 'children')],
    [Input('org-dropdown', 'value')]
)
def update_proposal_graph(org_id):
    if not org_id:
        raise PreventUpdate

    return __get_data_from_metric(service.get_metric_new_proposals(org_id))