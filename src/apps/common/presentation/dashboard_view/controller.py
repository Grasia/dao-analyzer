"""
   Descp: Dashboard view controller to manage the callbacks.

   Created on: 22-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from dash.dependencies import Input, Output, State

from src.apps.common.resources.strings import TEXT

def bind_callbacks(app, section_id: str) -> None:

    @app.callback(
         Output(section_id, 'children'),
        [Input('org-dropdown', 'value')],
        [State('org-dropdown', 'options')]
    )
    def organization_section_name(value: str, options: dict) -> str:
        if not value:
            return TEXT['no_data_selected']

        result = list(filter(lambda x: x['value'] == value, options))

        return result[0]['label']
