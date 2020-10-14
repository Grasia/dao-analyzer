"""
   Descp: Main view controller to manage the callbacks.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from src.apps.common.presentation.main_view.main_view import generate_layout
import src.apps.daostack.business.app_service as daostack
import src.apps.daohaus.business.app_service as daohaus
from src.apps.common.resources.strings import TEXT

def bind_callbacks(app) -> None:

    # Callbacks need to be loaded twice. 
    daostack.get_service().get_layout()
    daohaus.get_service().get_layout()


    @app.callback(
         Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        #print(pathname)
        if pathname == TEXT['url_main']:
            return generate_layout(
                header_title=TEXT['app_title'], 
                has_foot=False)
        elif pathname == TEXT['url_daostack']:
            return generate_layout(
                header_title=TEXT['app_title_daostack'],
                app_color=TEXT['css_color_daostack'],
                body=daostack.get_service().get_layout())
        elif pathname == TEXT['url_daohaus']:
            return generate_layout(
                header_title=TEXT['app_title_daohaus'],
                app_color=TEXT['css_color_daohaus'],
                body=daohaus.get_service().get_layout())
        else:
            return TEXT['not_found']


    @app.callback(
        Output('url', 'pathname'),
        [Input('daostack-bt', 'n_clicks'),
         Input('daohaus-bt', 'n_clicks')]
    )
    def load_ecosystem(bt_daostack: int, bt_daohaus: int) -> str:
        ctx = dash.callback_context

        if not bt_daostack and not bt_daohaus:
            raise PreventUpdate
        
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        
        pathname: str = TEXT['url_main']
        if trigger == 'daostack-bt':
            pathname = TEXT['url_daostack']
        elif trigger == 'daohaus-bt':
            pathname = TEXT['url_daohaus']

        return pathname
