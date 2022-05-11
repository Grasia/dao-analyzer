"""
   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os
from typing import Dict, List, Callable
from datetime import date
from dash import dcc, html
import dash_bootstrap_components as dbc
from dao_analyzer.apps.common.business.transfers.organization import OrganizationList

from dao_analyzer.apps.common.resources.strings import TEXT
from dao_analyzer.apps.common.presentation.main_view.main_view import REL_PATH

__ECOSYSTEM_SELECTED: Dict[str, List[str]] = {
    'default': ['', '', ''],
    'daostack': ['daostack-selected', '', ''],
    'aragon': ['', 'aragon-selected', ''],
    'daohaus': ['', '', 'daohaus-selected'],
}

def generate_layout(organizations: OrganizationList, sections: Dict, datapoints, ecosystem: str, update: str, org_id: str, org_value: str) -> List:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    if not org_value:
        org_value = organizations.get_all_orgs_dict()["value"]

    # TODO: Instead of using an <hr>, make two different containers, and put a gap between them
    return html.Div([
        dbc.Container(
            __generate_header(organizations, ecosystem, update, org_value),
        className='top-body'),
        dbc.Container([
            __generate_subheader(org_id, datapoints),
            __generate_sections(sections, id=f'{org_id}-body'),
        ], className='body'),
    ])

def __generate_header(organizations: OrganizationList, ecosystem: str, update: str, org_value: str) -> html.Div:
    selected: List[str] = __ECOSYSTEM_SELECTED['default']
    if ecosystem in __ECOSYSTEM_SELECTED.keys():
        selected = __ECOSYSTEM_SELECTED[ecosystem]

    return html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Span(TEXT['ecosystem_selector_title']),
                html.Span(f"({TEXT['last_update']} {update})", className='xsmall-font'),
            ], className='flex-column'),
            html.Div(children=[
                html.Div(children=[
                    html.Div(className='ecosystem-overlay daostack-color',
                        id='daostack-bt'),
                    html.Img(src=os.path.join(REL_PATH, TEXT['daostack_image_name']),
                        className='ecosystem-img flex-size-1'),
                ], className=f'ecosystem daostack-ecosystem {selected[0]}'),
                html.Div(children=[
                    html.Div(className='ecosystem-overlay aragon-color', 
                        id='aragon-bt'),
                    html.Img(src=os.path.join(REL_PATH, TEXT['aragon_image_name']),
                        className='ecosystem-img flex-size-1'),
                ], className=f'ecosystem aragon-ecosystem {selected[1]}'),
                html.Div(children=[
                    html.Div(className='ecosystem-overlay daohaus-color',
                        id='daohaus-bt'),
                    html.Img(src=os.path.join(REL_PATH, TEXT['daohaus_image_name']),
                        className='ecosystem-img flex-size-1'),
                ], className=f'ecosystem daohaus-ecosystem {selected[2]}'),
            ], className='flex-row flex-space-evenly flex-size-3')

        ], className='flex-row flex-size-1 flex-space-around'),

        html.Div(children=[
            html.Div(className='v-separator'),
            html.Div([
                html.Span(TEXT['dao_selector_title']),
                dcc.Dropdown(
                    id='org-dropdown',
                    options=organizations.get_dict_representation(),
                    value=org_value,
                    clearable=False,
                ),
            ], className='flex-column w-100'),
            dcc.Store(
                id='org-store',
                data=organizations,
                storage_type='memory',
            ),
        ], className='flex-row body-header-right'),

    ], className='body-header p-4 flex-row')

### SUBHEADER THINGS
def _get_dao_info(name: str, network: str, addr: str) -> html.Div:
    grid: List[html.Div] = [
        html.Div("Name", className='dao-info-label'),
        html.Div(name, className='dao-info-name'),
        html.Div("Network", className='dao-info-label'),
        html.Div(network, className='dao-info-network'),
        html.Div("Address", className='dao-info-label'),
        html.Div(html.Span(addr, className='address'), className='dao-info-address'),
    ]
    
    return html.Div(grid, className='dao-info-container')

def _gen_sum_hdr(creation_date: date = None):
    if creation_date:
        return html.Span(['Created on ', html.B(creation_date.strftime(TEXT['creation_date_format']))])
    else:
        return None

def _get_dao_summary_layout(org_id, datapoints: Dict, creation_date: date = None):
    dp_divs: List[html.Div] = [ dp.get_layout() for dp in datapoints.values() ]

    return html.Div([
        html.Div(_gen_sum_hdr(creation_date), className='dao-summary-hdr', id=org_id+'-summary-hdr'),
        html.Div(dp_divs, className='dao-summary-body'),
    ], className='dao-summary-container', style={'padding': '1em'})

def __generate_subheader(org_id: str, datapoints: Dict[str, List[Callable]]) -> dbc.Row:
    return dbc.Row(
        id=org_id,
        className='my-3',
        children=html.Div([
           html.Div(html.Div(TEXT['no_data_selected'], className='dao-info-name'), id=org_id+'-info'),
           _get_dao_summary_layout(org_id, datapoints)
        ], className='dao-header-container pt-4'),
    )

def __generate_sections(sections: Dict[str, List[Callable]], id=None) -> dbc.Row:
    tabs: List[dcc.Tab] = []

    for name, data in sections.items():
        charts = list()
        for chart_pane in data['callables']:
            charts.append(chart_pane())

        sec_hdr = dbc.Row(
            [html.Div(name, className='section-title')],
            id=f'{data["css_id"]}-hdr', 
            className='section-hdr'
        )

        if 'disclaimer' in data and data['disclaimer']:
            sec_hdr.children.append(html.Div(data['disclaimer'], className='section-disclaimer'))

        container = dbc.Container(
            class_name='g-4',
            children=[
                sec_hdr,
                dbc.Row(children=charts, className='row-cols-1 row-cols-xl-2'),
            ],
        )

        tabs.append(dcc.Tab(label=name, children=container))

    return dbc.Row(dcc.Tabs(tabs, parent_className='g-0'), id=id)
