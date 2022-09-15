"""
   Descp: Dashboard view controller to manage the callbacks.

   Created on: 22-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import Tuple

from dash import html
from dash.dependencies import Input, Output, State
from dao_analyzer.web.apps.common.business.transfers import Organization, OrganizationList, Platform

from dao_analyzer.web.apps.common.presentation.dashboard_view.dashboard_view import _get_dao_info, _get_platform_info, _gen_sum_hdr


# We use organizations Data Access Object to be able to update the organization
# list every callback
def bind_callbacks(app, section_id: str) -> None:
    dao_info_id = section_id + '-info'
    dao_sum_hdr = section_id + '-summary-hdr'

    @app.callback(
        Output(dao_info_id, 'children'),
        Output(dao_sum_hdr, 'children'),
        Input('org-dropdown', 'value'),
        Input('platform-info-store', 'data'),
        State('organization-list-store', 'data'),
    )
    def organization_section_name(value: str, platform_info: dict, org_list: list) -> Tuple[html.Div, html.Div]:
        """This callback is called when the card should change

        Args:
            value (str): The id of the dao selected in the dropdown
            platform_info (dict): The platform info, aggregation of all DAOs
            org_list (list): The list of organizations and its data to be shown on dao-info-container

        Returns:
            Tuple: The dao-info-container and dao card header
        """
        if not value:
            return _get_platform_info(None), _gen_sum_hdr()

        organization_list = OrganizationList.from_json(org_list)        

        if organization_list.is_all_orgs(value):
            return _get_platform_info(Platform.from_json(platform_info)), _gen_sum_hdr()

        result: Organization = next((x for x in organization_list if x.get_id() == value))
        
        return _get_dao_info(result), _gen_sum_hdr(result)

    @app.callback(
        Output(f'{section_id}-body', 'className'),
        Input(f'{section_id}-body', 'className'),
        Input('org-dropdown', 'value'),
        State('organization-list-store', 'data'),
    )
    def show_hide_plots(cname: str, value: str, org_list: list):
        if not value:
            return cname

        if not cname:
            cname = ''

        classes = set(filter(None, cname.split(' ')))
    
        orgs = OrganizationList.from_json(org_list)
        if orgs.is_all_orgs(value):
            # Hide the ones with only-on-dao
            classes.add('is-all-orgs')
        else:
            classes.discard('is-all-orgs')
        
        return ' '.join(classes)
