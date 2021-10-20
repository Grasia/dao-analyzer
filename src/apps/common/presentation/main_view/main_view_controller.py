"""
   Descp: Main view controller to manage the callbacks.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import logging

from src.apps.common.presentation.main_view.main_view import generate_layout
import src.apps.daostack.business.app_service as daostack
import src.apps.daohaus.business.app_service as daohaus
import src.apps.aragon.business.app_service as aragon
from src.apps.common.resources.strings import TEXT

def bind_callbacks(app) -> None: # noqa: C901

    # Callbacks need to be loaded twice. 
    service_daostack = daostack.DaostackService()
    service_daohaus = daohaus.DaohausService()
    service_aragon = aragon.AragonService()

    service_daostack.bind_callbacks()
    service_daohaus.bind_callbacks()
    service_aragon.bind_callbacks()

    @app.callback(
        [Output('page-content', 'children'),
         Output('header-loading-state', 'children')],
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        content = TEXT['not_found']
        state = 'loading'

        patharr = pathname.split("/")
        platform = patharr[1] if len(patharr) >= 2 else TEXT['url_main']
        network = patharr[2] if len(patharr) >= 4 else None
        dao_id = patharr[3] if len(patharr) >= 4 else None

        logging.info(f"request with platform: {platform}, network: {network}, dao: {dao_id}")

        if platform == TEXT['url_daostack']:
            content = generate_layout(body=service_daostack.get_layout())
        elif platform == TEXT['url_main'] or platform == TEXT['url_daohaus']:
            content = generate_layout(body=service_daohaus.get_layout())
        elif platform == TEXT['url_aragon']:
            content = generate_layout(body=service_aragon.get_layout())
        
        return [content, state]


    @app.callback(
        Output('url', 'pathname'),
        [Input('daostack-bt', 'n_clicks'),
         Input('daohaus-bt', 'n_clicks'),
         Input('aragon-bt', 'n_clicks')]
    )
    def load_ecosystem(bt_daostack: int, bt_daohaus: int, bt_aragon: int) -> str:
        ctx = dash.callback_context

        if not bt_daostack and not bt_daohaus and not bt_aragon:
            raise PreventUpdate
        
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        
        pathname: str = TEXT['url_main']
        if trigger == 'daostack-bt':
            pathname = TEXT['url_daostack']
        elif trigger == 'daohaus-bt':
            pathname = TEXT['url_daohaus']
        elif trigger == 'aragon-bt':
            pathname = TEXT['url_aragon']

        return "/" + pathname
