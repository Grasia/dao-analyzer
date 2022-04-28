"""
   Descp: Dashboard view controller to manage the callbacks.

   Created on: 22-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import List

from datetime import date

from dash import html
from dash.dependencies import Input, Output, State
from dao_analyzer.apps.common.data_access.daos.organization_dao import OrganizationListDao

from dao_analyzer.apps.common.resources.strings import TEXT

def _get_dao_info(name: str, network: str, addr: str) -> html.Div:
    grid: List[html.Div] = [
        html.Div("Name", className='dao-info-label'),
        html.Div(name, className='dao-info-name'),
        html.Div("Network", className='dao-info-label'),
        html.Div(network, className='dao-info-network'),
        html.Div("Address", className='dao-info-label'),
        html.Div(html.Span(addr, className='address'), className='dao-info-address'),
    ]
    
    return html.Div(grid, className='dao-info grid-container', style={
        'grid-template-columns': '100px 1fr',
    })

def _get_data_point(title: str, number: str, evolution: str) -> html.Div:
    if evolution.startswith('-'):
        icon = html.I(className='fa-solid fa-circle-down fa-xs dp-icon-down')
    else:
        icon = html.I(className='fa-solid fa-circle-up fa-xs dp-icon-up')
    
    return html.Div([
        html.Span(title, className='dao-summary-datapoint-title'),
        html.Div(number, className='dao-summary-datapoint-number'),
        html.Div('Last month', className='dao-summary-datapoint-lastmonth'),
        html.Div([icon, " ", evolution], className='dao-summary-datapoint-evolution'),
    ], className='dao-summary-datapoint')

def _get_dao_summary(creation_date: date, members: float, treasury: float, proposals: float):
    hdr = html.Div(html.Span(['Creation date: ', html.B(creation_date.isoformat())]), className='dao-summary-hdr')

    # TODO: Remove placeholders and pass values
    rest = html.Div([
        _get_data_point('Members', "12.6k", "8"),
        _get_data_point('Treasury', "$2.3", "-$2100"),
        _get_data_point('Proposals', "6", "1"),
    ], className='dao-summary-body')
    return html.Div([
        hdr,
        rest,
    ], className='dao-summary-container', style={'padding': '1em'})

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

        return html.Div([
            _get_dao_info(name, result.get_network(), result.get_id()),
            # TODO: Remove placeholder values
            _get_dao_summary(date.today(), 12.6e3, 2.3e6, 42),
        ], className='dao-header-container')
