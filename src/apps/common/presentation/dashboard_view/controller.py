"""
   Descp: Dashboard view controller to manage the callbacks.

   Created on: 22-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from dash.dependencies import Input, Output, State
from src.apps.common.business.transfers.organization import OrganizationList

from src.apps.common.resources.strings import TEXT


def bind_callbacks(app, section_id: str, organizations: OrganizationList) -> None:

    @app.callback(
        Output(section_id, 'children'),
        [Input('org-dropdown', 'value')],
        [State('org-dropdown', 'options')]
    )
    def organization_section_name(value: str, options: dict) -> str:
        if not value:
            return TEXT['no_data_selected']

        if organizations.is_all_orgs(value):
            return options[0]["label"]
        
        result = next((x for x in organizations if x.get_id() == value))
        return result.get_label_long()
