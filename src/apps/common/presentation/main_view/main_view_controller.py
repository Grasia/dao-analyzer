"""
   Descp: Main view controller to manage the callbacks.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import src.apps.daostack.business.app_service as daostack
import src.apps.daohaus.business.app_service as daohaus


def bind_callback(app) -> None:

    @app.callback(
         Output('page-content', 'children'),
        [Input('daostack-bt', 'n_clicks')]
    )
    def load_daostack(n_clicks):
        if not n_clicks:
            raise PreventUpdate

        return daostack.get_service().get_layout()


    @app.callback(
         Output('page-content', 'children'),
        [Input('daohaus-bt', 'n_clicks')]
    )
    def load_daohaus(n_clicks):
        if not n_clicks:
            raise PreventUpdate

        return daohaus.get_service().get_layout()


# TODO: issue 15
# @app.callback( Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     print(pathname)
#     if pathname == '/apps/daostack' or '/':
#         return get_service().get_layout()
#     else:
#         return '404'
