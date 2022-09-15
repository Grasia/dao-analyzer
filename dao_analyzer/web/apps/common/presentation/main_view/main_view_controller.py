"""
   Descp: Main view controller to manage the callbacks.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict, Any

import dash
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dao_analyzer.web.apps.common.business.transfers.organization.organization_filter import ALL_NETWORKS_VALUE
from dao_analyzer.web.apps.common.business.transfers.organization.organization_list import OrganizationList

from dao_analyzer.web.apps.common.presentation.main_view.main_view import generate_layout
import dao_analyzer.web.apps.common.presentation.about_view.about_view as about
import dao_analyzer.web.apps.daostack.business.app_service as daostack
import dao_analyzer.web.apps.daohaus.business.app_service as daohaus
import dao_analyzer.web.apps.aragon.business.app_service as aragon
from dao_analyzer.web.apps.common.resources.strings import TEXT

ABOUT_SUBPAGE: str = '__about'

def _process_params(search: str) -> Dict[str, str]:
    # TODO: Return Dict[str, Any] instead (parse json)
    search = search.removeprefix('?')

    if not search:
        return {}
    
    params = dict()
    for p in search.split('&'):
        k,v = p.split('=', 1) # Split only on first ocurrence
        params[k] = v

    if 'filters' in params:
        params['filters'] = params['filters'].split(',')

    return params

def _params_string(d: Dict[str, str]):
    if not d: 
        return ""

    if 'filters' in d:
        d['filters'] = ','.join(d['filters'])

    return '?' + '&'.join(['='.join([k,v]) for k,v in d.items()])

def bind_callbacks(app) -> None: # noqa: C901

    # Callbacks need to be loaded twice.
    services: Dict[str, Any] = {
        "daostack": daostack.DaostackService(),
        "daohaus": daohaus.DaohausService(),
        "aragon": aragon.AragonService(),
    }

    for s in services.values():
        s.bind_callbacks(app)

    @app.callback(
        Output('page-content', 'children'),
        Output('header-loading-state', 'children'), # <- THIS CAUSES THE FLASH
        Input('page-content', 'data-subpage'),
        State('page-content', 'data-org-id'),
        State('url', 'search'),
    )
    def change_subpage(subpage, org_id, search):
        if not subpage:
            return dcc.Location(pathname='/daohaus', id='default_redirect'), 'redirect'
        elif subpage == ABOUT_SUBPAGE:
            return generate_layout(body=about.get_layout()), ''
        elif subpage in services:
            params = _process_params(search)

            return generate_layout(body=services[subpage].get_layout(
                org_value=org_id, 
                network_value=params.get('network', None),
                filter_values=params.get('filters', []),
            )), 'loading'

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
            organizations = services[platform].organization_list()

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
        Output('platform-info-store', 'data'),
        Output('url', 'search'),
        Input('org-filter', 'value'),
        Input('org-network-radio', 'value'),
        State('org-dropdown', 'value'),
        State('organization-list-store', 'data'),
        State('page-content', 'data-subpage'),
    )
    def org_filters(filter_values: List[str], network_value: str, org_value: str, org_list: list, platform_name: str):
        filtered = OrganizationList.from_json(org_list)

        # First we initialize all values
        organizations = filtered.filter(filter_values, network_value, only_enabled=True)
        options = organizations.get_dict_representation()
        org_number = f"There are {len(organizations):,} DAOs"
        platform = dash.no_update
        params = {}
        
        if network_value != ALL_NETWORKS_VALUE:
            params['network'] = network_value
        
        ndf = OrganizationList.get_diff_filters(filter_values)
        if ndf:
            params['filters'] = [ f.id for f in ndf ]

        # If the selected DAO was filtered out, fall back to All DAOs
        if org_value in [ x['value'] for x in options ]:
            value = org_value
        else:
            value = organizations.get_all_orgs_dict()['value']

        # Change only if is all orgs
        if value == organizations.ALL_ORGS_ID:
            platform = services[platform_name].platform(organizations)

        return options, value, org_number, platform, _params_string(params)
