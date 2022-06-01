"""
   Descp: Dashboard view controller to manage the callbacks.

   Created on: 22-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from dash import html
from dash.dependencies import Input, Output, State
from dao_analyzer.apps.common.business.transfers import Organization
from dao_analyzer.apps.common.business.transfers.organization.platform import Platform

from dao_analyzer.apps.common.resources.strings import TEXT
from dao_analyzer.apps.common.presentation.dashboard_view.dashboard_view import _get_dao_info, _get_platform_info, _gen_sum_hdr


# We use organizations Data Access Object to be able to update the organization
# list every callback
def bind_callbacks(app, section_id: str) -> None:
    dao_info_id = section_id + '-info'
    dao_sum_hdr = section_id + '-summary-hdr'

    @app.callback(
        Output(dao_info_id, 'children'),
        Output(dao_sum_hdr, 'children'),
        Input('org-dropdown', 'value'),
        State('org-dropdown', 'options'),
        State('platform-store', 'data'),
    )
    def organization_section_name(value: str, options: dict, platform_store: Platform) -> html.Div:
        if not value:
            return html.Div(TEXT['no_data_selected'], className='dao-info-name'), _gen_sum_hdr()

        platform = Platform.from_json(platform_store)
        if platform.is_all_orgs(value):
            return _get_platform_info(platform), _gen_sum_hdr()
        
        result: Organization = next((x for x in platform.organization_list if x.get_id() == value))
        
        return _get_dao_info(result), _gen_sum_hdr(result)

    @app.callback(
        Output(f'{section_id}-body', 'className'),
        Input(f'{section_id}-body', 'className'),
        Input('org-dropdown', 'value'),
        State('platform-store', 'data'),
    )
    def show_hide_plots(cname: str, value: str, plat_store: dict):
        if not value:
            return cname

        if not cname:
            cname = ''

        classes = set(filter(None, cname.split(' ')))
    
        orgs = Platform.from_json(plat_store).organization_list
        if orgs.is_all_orgs(value):
            # Hide the ones with only-on-dao
            classes.add('is-all-orgs')
        else:
            classes.discard('is-all-orgs')
        
        return ' '.join(classes)
