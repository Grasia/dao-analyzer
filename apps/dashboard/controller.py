"""
   controller.py

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
import apps.dashboard.daos.dao as DAO
from apps.dashboard.strings import TEXT


def get_layout() -> html.Div:
    daos: List[Dict[str, str]] = DAO.get_all_daos()
    labels: List[Dict[str, str]] = [{'value': obj['id'], 
        'label': obj['name']} for obj in daos]

    return ly.generate_layout(labels)



@app.callback(
    [Output('new-users-graph', 'figure'),
    Output('new-users-amount', 'children'),
    Output('new-users-subtitle', 'children')],
    [Input('dao-dropdown', 'value')]
)
def dao_selector(dao_id):
    if not dao_id:
        raise PreventUpdate

    data:Dict[str, List] = DAO.get_new_users_data(dao_id)

    if not data:
        if DEBUG:
            print(LOGS['graph_error'])
        raise PreventUpdate

    return [
        ly.generate_bar_chart(x=data['x'], y=data['y']),
        data['last_month_users'],
        TEXT['graph_subtitle'].format(data['last_month_name'], 
            data['month_over_month'])
    ]