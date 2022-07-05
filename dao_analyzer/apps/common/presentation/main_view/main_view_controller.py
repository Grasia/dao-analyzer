"""
   Descp: Main view controller to manage the callbacks.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import List

import dash
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dao_analyzer.apps.common.business.transfers.organization.platform import Platform

from dao_analyzer.apps.common.presentation.main_view.main_view import generate_layout
import dao_analyzer.apps.common.presentation.about_view.about_view as about
import dao_analyzer.apps.daostack.business.app_service as daostack
import dao_analyzer.apps.daohaus.business.app_service as daohaus
import dao_analyzer.apps.aragon.business.app_service as aragon
from dao_analyzer.apps.common.resources.strings import TEXT

ABOUT_SUBPAGE: str = '__about'

def bind_callbacks(app) -> None: # noqa: C901

    # Callbacks need to be loaded twice.
    services = {
        "daostack": daostack.DaostackService(),
        "daohaus": daohaus.DaohausService(),
        "aragon": aragon.AragonService()
    }

    for s in services.values():
        s.bind_callbacks(app)

    @app.callback(
        Output('page-content', 'children'),
        Output('header-loading-state', 'children'), # <- THIS CAUSES THE FLASH
        Input('page-content', 'data-subpage'),
        State('page-content', 'data-org-id'),
    )
    def change_subpage(subpage, org_id):
        if not subpage:
            return dcc.Location(pathname='/daohaus', id='default_redirect'), 'redirect'
        elif subpage == ABOUT_SUBPAGE:
            return generate_layout(body=about.get_layout()), ''
        elif subpage in services:
            return generate_layout(body=services[subpage].get_layout(org_id)), 'loading'

    @app.callback(
        Output('page-content', 'data-subpage'),
        Output('page-content', 'data-org-id'),
        Input('url', 'pathname'),
        State('page-content', 'data-subpage')
    )
    def url_changed(pathname, current_platform):
        if pathname == "/":
            return '', dash.no_update

        if pathname == '/' + TEXT['url_about']:
            return ABOUT_SUBPAGE, dash.no_update

        patharr = pathname.split("/")

        platform = patharr[1]
        org_id = patharr[2] if len(patharr) >= 3 else None

        # Dont regenerate layout if we are already using it
        if platform == current_platform:
            raise PreventUpdate

        return platform, org_id

    @app.callback(
        Output('url', 'pathname'),
        Input('daostack-bt', 'n_clicks'),
        Input('daohaus-bt', 'n_clicks'),
        Input('aragon-bt', 'n_clicks'),
        Input('org-dropdown', 'value'),
        State('url', 'pathname')
    )
    def load_ecosystem(bt_daostack: int, bt_daohaus: int, bt_aragon: int, dropdown_value: str, prev_pathname: str) -> str:
        ctx = dash.callback_context

        # prev_pathname state changed (maybe we did it)
        if not bt_daostack and not bt_daohaus and not bt_aragon and not dropdown_value:
            raise PreventUpdate
        # dropdown_value changed
        elif not bt_daostack and not bt_daohaus and not bt_aragon:
            platform = prev_pathname.split("/")[1]
            organizations = services[platform].platform().organization_list

            new_pathname = f'/{platform}'

            if not organizations.is_all_orgs(dropdown_value):
                new_pathname += f'/{dropdown_value}'

            if new_pathname == prev_pathname:
                raise PreventUpdate

            return new_pathname
        
        trigger = ctx.triggered_id
        
        pathname: str = "/"
        if trigger == 'daostack-bt':
            pathname = TEXT['url_daostack']
        elif trigger == 'daohaus-bt':
            pathname = TEXT['url_daohaus']
        elif trigger == 'aragon-bt':
            pathname = TEXT['url_aragon']

        return "/" + pathname

    @app.callback(
        Output('org-dropdown', 'options'),
        Output('org-dropdown', 'value'),
        Output('org-number', 'children'),
        Input('org-filter', 'value'),
        Input('org-network-filter', 'value'),
        State('org-dropdown', 'value'),
        State('platform-store', 'data'),
    )
    def org_filters(filter_values: List[str], network_values: List[str], org_value: str, plat_store: dict):
        filtered = Platform.from_json(plat_store).organization_list

        organizations = filtered.filter(filter_values, network_values, only_enabled=True)
        options = organizations.get_dict_representation()
        org_number = f"There are {len(organizations):,} DAOs"

        # If the selected DAO was filtered out, fall back to All DAOs
        if org_value in [ x['value'] for x in options ]:
            value = org_value
        else:
            value = organizations.get_all_orgs_dict()['value']

        return options, value, org_number
