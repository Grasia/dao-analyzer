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

# We use organizations Data Access Object to be able to update the organization
# list every callback
def bind_callbacks(app, section_id: str, organizationsDAO: OrganizationListDao) -> None:

    @app.callback(
        Output(section_id, 'children'),
        [Input('org-dropdown', 'value')],
        [State('org-dropdown', 'options')]
    )
    def organization_section_name(value: str, options: dict) -> html.Div:
        if not value:
            return html.Div(TEXT['no_data_selected'], className='dao-info-name')

        organizations = organizationsDAO.get_organizations()
        if organizations.is_all_orgs(value):
            return html.Div(options[0]["label"], className='dao-info-name')
        
        result = next((x for x in organizations if x.get_id() == value))
        
        name = html.I(TEXT['unknown_dao_name'])
        if result.get_name():
            name = result.get_name()

        return [
            html.Div('Name', className='dao-info-label'),
            html.Div(name, className='dao-info-name'),
            html.Div('Network', className='dao-info-label'),
            html.Div(result.get_network(), className='dao-info-network'),
            html.Div('Address', className='dao-info-label'),
            html.Div(html.Span(result.get_id(), className='address'), className='dao-info-address')
        ]
