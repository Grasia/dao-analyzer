"""
   Descp: It's used to manage the dashboard events.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict

from dash.dependencies import Input, Output
import dash_html_components as html
from dash.exceptions import PreventUpdate

from app import app
from app import DEBUG
from logs import LOGS
import apps.dashboard.layout as ly
from apps.dashboard.strings import TEXT
from apps.dashboard.domain.daos.dao_organization import get_all_orgs
from apps.dashboard.domain.daos.dao_new_user_metric import get_new_users_metric
import apps.dashboard.domain.transfers as tr


def get_layout() -> html.Div:
    orgs: List[tr.Organization] = get_all_orgs()
    labels: List[Dict[str, str]] = \
        [{'value': o.id, 'label': o.name} for o in orgs]

    return ly.generate_layout(labels)



@app.callback(
    [Output('new-users-graph', 'figure'),
    Output('new-users-amount', 'children'),
    Output('new-users-subtitle', 'children')],
    [Input('org-dropdown', 'value')]
)
def dao_selector(org_id):
    if not org_id:
        raise PreventUpdate

    metric: tr.MetricNewUsers = get_new_users_metric(org_id)

    return [
        ly.generate_bar_chart(x = metric.x, y = metric.y),
        metric.last_month_n_users,
        TEXT['graph_subtitle'].format(metric.last_month_name, 
            metric.month_over_month)
    ]