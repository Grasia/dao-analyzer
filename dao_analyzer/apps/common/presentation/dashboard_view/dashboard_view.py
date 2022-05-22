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

    return html.Div([
        dbc.Container(
            __generate_header(organizations, ecosystem, update, org_value),
        className='top body mb-3 py-4'),
        dbc.Container([
            __generate_subheader(org_id, datapoints),
            __generate_sections(sections),
        ], className='body', id=f'{org_id}-body'),
    ])

def __gen_ecosystem(id: str, selected: str) -> html.Div:
    return html.Div(children=[
        html.Div(className=f'ecosystem-overlay {id}-color',
            id=f'{id}-bt'),
        html.Img(src=os.path.join(REL_PATH, TEXT[f'{id}_image_name']),
            className='ecosystem-img'),
    ], className=f'ecosystem {id}-ecosystem {selected}')

def __generate_header(organizations: OrganizationList, ecosystem: str, update: str, org_value: str) -> dbc.Row:
    selected: List[str] = __ECOSYSTEM_SELECTED['default']
    if ecosystem in __ECOSYSTEM_SELECTED.keys():
        selected = __ECOSYSTEM_SELECTED[ecosystem]

    ecosystems: List[html.Div] = [ __gen_ecosystem(eid, selected[i]) for i,eid in enumerate(['daostack', 'aragon', 'daohaus']) ]

    return dbc.Row(children=[
        html.Div(children=[
            html.Div(TEXT['ecosystem_selector_title']),
            html.Div(children=ecosystems, className='ecosystems-wrapper'),
        ], className='col d-flex flex-row align-items-center justify-content-between gap-3'),
        html.Div(children=[
            html.Div(html.Span(TEXT['dao_selector_title'])),
            html.Div([
                html.Div(f"There are {len(organizations):,} DAOs", id='org-number', className='number-of-daos'),
                html.Div(dcc.Dropdown(
                    id='org-dropdown',
                    options=organizations.get_dict_representation(),
                    value=org_value,
                    clearable=False,
                )),
            ], className='flex-grow-1')
        ], className='col d-flex flex-row justify-content-between align-items-center gap-3'),
        dcc.Store(
            id='org-store',
            data=organizations,
            storage_type='memory',
        ),
        html.Div(f'Last update: {update}', className='last-update'),
    ], className='body-header row-divider')

### SUBHEADER THINGS
def _get_dao_info(name: str, network: str, addr: str, creation_date: date = None) -> html.Div:
    grid: List[html.Div] = [
        html.Div("Name", className='dao-info-label'),
        html.Div(name, className='dao-info-name'),
        html.Div("Network", className='dao-info-label'),
        html.Div(network, className='dao-info-network'),
        html.Div("Address", className='dao-info-label'),
        html.Div(html.Span(addr, className='address'), className='dao-info-address'),
    ]

    if creation_date:
        grid.append(html.Div("Creation Date", className='dao-info-label'))
        grid.append(html.Div(creation_date.strftime(TEXT['creation_date_format']), className='dao-info-date'))
    
    return html.Div(grid, className='dao-info-container')

def _gen_sum_hdr(last_activity: date = None):
    if last_activity:
        if last_activity == date.min:
            return html.Span(['Has ', html.B('never'), ' been active'])
        return html.Span(['Last active on ', html.B(last_activity.strftime(TEXT['last_activity_format']))])
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

def __generate_sections(sections: Dict[str, List[Callable]]) -> dbc.Row:
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

    return dcc.Tabs(tabs)
