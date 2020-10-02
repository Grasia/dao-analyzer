"""
   Descp: Main view controller to manage the callbacks.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import src.apps.daostack.business.app_service as daostack
import src.apps.daohaus.business.app_service as daohaus
from src.apps.common.presentation.main_view.main_view import generate_foot


def bind_callbacks(app) -> None:

    @app.callback(
        [Output('body', 'children'),
         Output('foot', 'children')],
        [Input('daostack-bt', 'n_clicks'),
         Input('daohaus-bt', 'n_clicks')]
    )
    def load_ecosystem(_, _2) -> list:
        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate

        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        
        body: list = []
        if trigger == 'daostack-bt':
            body = daostack.get_service().get_layout()
        elif trigger == 'daohaus-bt':
            body = daohaus.get_service().get_layout()

        return [body, generate_foot()]


# TODO: issue 15
# @app.callback( Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     print(pathname)
#     if pathname == '/apps/daostack' or '/':
#         return get_service().get_layout()
#     else:
#         return '404'
