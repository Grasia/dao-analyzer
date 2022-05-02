"""
   Descp: Dashboard view controller to manage the callbacks.

   Created on: 22-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from dash import html
from dash.dependencies import Input, Output, State
from dao_analyzer.apps.common.data_access.daos.organization_dao import OrganizationListDao

from dao_analyzer.apps.common.resources.strings import TEXT
from dao_analyzer.apps.common.presentation.dashboard_view.dashboard_view import _get_dao_info, _gen_sum_hdr


# We use organizations Data Access Object to be able to update the organization
# list every callback
def bind_callbacks(app, section_id: str, organizationsDAO: OrganizationListDao) -> None:
    dao_info_id = section_id + '-info'
    dao_sum_hdr = section_id + '-summary-hdr'

    @app.callback(
        Output(dao_info_id, 'children'),
        Output(dao_sum_hdr, 'children'),
        [Input('org-dropdown', 'value')],
        [State('org-dropdown', 'options')]
    )
    def organization_section_name(value: str, options: dict) -> html.Div:
        if not value:
            return html.Div(TEXT['no_data_selected'], className='dao-info-name'), _gen_sum_hdr()

        organizations = organizationsDAO.get_organizations()
        if organizations.is_all_orgs(value):
            return html.Div(options[0]["label"], className='dao-info-name'), _gen_sum_hdr()
        
        result = next((x for x in organizations if x.get_id() == value))
        
        name = html.I(TEXT['unknown_dao_name'])
        if result.get_name():
            name = result.get_name()

        return _get_dao_info(name, result.get_network(), result.get_id()), _gen_sum_hdr(result.get_creation_date())
