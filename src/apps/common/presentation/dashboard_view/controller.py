"""
   Descp: Dashboard view controller to manage the callbacks.

   Created on: 22-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from dash.dependencies import Input, Output, State
from src.apps.common.data_access.daos.organization_dao import OrganizationListDao

from src.apps.common.resources.strings import TEXT

# We use organizations Data Access Object to be able to update the organization
# list every callback
def bind_callbacks(app, section_id: str, organizationsDAO: OrganizationListDao) -> None:

    @app.callback(
        Output(section_id, 'children'),
        [Input('org-dropdown', 'value')],
        [State('org-dropdown', 'options')]
    )
    def organization_section_name(value: str, options: dict) -> str:
        if not value:
            return TEXT['no_data_selected']

        organizations = organizationsDAO.get_organizations()
        if organizations.is_all_orgs(value):
            return options[0]["label"]
        
        result = next((x for x in organizations if x.get_id() == value))
        return result.get_label_long()
