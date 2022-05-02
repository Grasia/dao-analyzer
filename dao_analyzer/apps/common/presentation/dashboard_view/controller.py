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

def _get_dp_icon(evolution: str):
    if evolution.startswith('-'):
        return html.I(className='fa-solid fa-circle-down fa-xs dp-icon-down')
    else:
        return html.I(className='fa-solid fa-circle-up fa-xs dp-icon-up')

def _get_dp_children(title: str = "?", number: str = "?", evolution: str = "?", id: str = ""):
    return [
        html.Span(title, className='dao-summary-datapoint-title'),
        html.Div(number, className='dao-summary-datapoint-number', id=id+'-number'),
        html.Div('This month', className='dao-summary-datapoint-lastmonth'),
        html.Div([_get_dp_icon(evolution), " ", evolution], className='dao-summary-datapoint-evolution', id=id+'-evolution'),
    ]

def _get_dao_summary_layout(section_id, creation_date: date = None):
    if creation_date:
        hdr = html.Div(html.Span(['Creation date: ', html.B(creation_date.isoformat())]), className='dao-summary-hdr')
    else:
        hdr = None

    rest = html.Div([
        html.Div(_get_dp_children('Members', id=section_id+'-dp-members'), className='dao-summary-datapoint', id=section_id+'-dp-members'),
        html.Div(_get_dp_children('Treasury', id=section_id+'-dp-treasury'), className='dao-summary-datapoint', id=section_id+'-dp-treasury'),
        html.Div(_get_dp_children('Proposals', id=section_id+'-dp-proposals'), className='dao-summary-datapoint', id=section_id+'-dp-proposals'),
    ], className='dao-summary-body', id=section_id+'-dp')
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
            _get_dao_summary_layout(section_id, result.get_creation_date()),
        ], className='dao-header-container')
