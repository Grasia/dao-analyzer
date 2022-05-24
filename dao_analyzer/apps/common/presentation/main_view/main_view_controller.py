"""
   Descp: Main view controller to manage the callbacks.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import dash
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dao_analyzer.apps.common.business.transfers.organization import OrganizationList

from dao_analyzer.apps.common.presentation.main_view.main_view import generate_layout
import dao_analyzer.apps.common.presentation.about_view.about_view as about
import dao_analyzer.apps.daostack.business.app_service as daostack
import dao_analyzer.apps.daohaus.business.app_service as daohaus
import dao_analyzer.apps.aragon.business.app_service as aragon
from dao_analyzer.apps.common.resources.strings import TEXT

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
        Output('header-loading-state', 'children'),
        Output('page-content', 'data-current-platform'),
        Input('url', 'pathname'),
        State('page-content', 'data-current-platform')
    )
    def display_page(pathname, current_platform):
        if pathname == "/":
            return [dcc.Location(pathname="/daohaus", id="default_redirect"), "redirect", "daohaus"]

        if pathname == '/' + TEXT['url_about']:
            return generate_layout(body=about.get_layout()), '', 'about'

        content = TEXT['not_found']
        state = 'loading'

        patharr = pathname.split("/")

        platform = patharr[1]
        value = patharr[2] if len(patharr) >= 3 else None

        # Dont regenerate layout if we are already using it
        if platform == current_platform:
            raise PreventUpdate

        if platform in services:
            content = generate_layout(body=services[platform].get_layout(value))
        
        return content, state, platform


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
            organizations = services[platform].organizations()

            new_pathname = f'/{platform}'

            if not organizations.is_all_orgs(dropdown_value):
                new_pathname += f'/{dropdown_value}'

            if new_pathname == prev_pathname:
                raise PreventUpdate

            return new_pathname
        
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        
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
        State('org-dropdown', 'value'),
        State('org-store', 'data'),
    )
    def org_filters(filter_values: list[str], org_value: str, org_store: list):
        filtered = OrganizationList(org_store)

        for f in OrganizationList.get_filters(filter_values, only_enabled=True):
            filtered = filter(f.pred, filtered)

        organizations = OrganizationList(filtered)
        options = organizations.get_dict_representation()
        org_number = f"There are {len(organizations):,} DAOs"

        # If the selected DAO was filtered out, fall back to All DAOs
        if org_value in [ x['value'] for x in options ]:
            value = org_value
        else:
            value = organizations.get_all_orgs_dict()['value']

        return options, value, org_number
