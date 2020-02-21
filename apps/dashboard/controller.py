"""
   controller.py

   Descp: It's used to manage the dashboard events.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from dash.dependencies import Input, Output
import dash_html_components as html

from app import app
from api_manager import get_all_daos
from apps.dashboard.layout import generate_layout


def get_layout() -> html.Div:
    labels: list = get_all_daos()
    return generate_layout(labels)


# @app.callback(
#     Output('app-1-display-value', 'children'),
#     [Input('dao-dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)