"""
   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os
from typing import Dict, List, Callable
from datetime import date
from dash import dcc
from dash import html

from dao_analyzer.apps.common.resources.strings import TEXT
from dao_analyzer.apps.common.presentation.main_view.main_view import REL_PATH

__ECOSYSTEM_SELECTED: Dict[str, List[str]] = {
    'default': ['', '', ''],
    'daostack': ['daostack-selected', '', ''],
    'aragon': ['', 'aragon-selected', ''],
    'daohaus': ['', '', 'daohaus-selected'],
}

def generate_layout(labels: List[Dict[str, str]], sections: Dict, datapoints, ecosystem: str, update: str, org_id: str, org_value: str) -> List:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    if not org_value:
        org_value = labels[0]["value"]

    return html.Div(children=[
        __generate_header(labels, ecosystem, update, org_value),
        html.Div(className='h-separator'),
        __generate_subheader(org_id, datapoints),
        __generate_sections(sections)
    ], className='main-body left-padding-aligner right-padding-aligner')
    

def __generate_header(labels: List[Dict[str, str]], ecosystem: str, update: str, org_value: str) -> html.Div:
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
            html.Div(className='v-separator flex-size-1'),
            html.Span(TEXT['dao_selector_title'], className=''),
            dcc.Dropdown(
                id='org-dropdown',
                options=labels,
                value=org_value,
                className='flex-size-3',
            )
        ], className='flex-row flex-size-1'),

    ], className='body-header small-padding flex-row')

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
    
    return html.Div(grid, className='dao-info grid-container', style={
        'grid-template-columns': '100px 1fr',
    })

def _gen_sum_hdr(creation_date: date = None):
    if creation_date:
        return html.Span(['Creation date: ', html.B(creation_date.isoformat())])
    else:
        return None

def _get_dao_summary_layout(org_id, datapoints: Dict, creation_date: date = None):
    dp_divs: List[html.Div] = [ dp.get_layout() for dp in datapoints.values() ]

    return html.Div([
        html.Div(_gen_sum_hdr(creation_date), className='dao-summary-hdr', id=org_id+'-summary-hdr'),
        html.Div(dp_divs, className='dao-summary-body'),
    ], className='dao-summary-container', style={'padding': '1em'})

def __generate_subheader(org_id: str, datapoints: Dict[str, List[Callable]]) -> html.Div:
    return html.Div(
        id=org_id,
        className='body small-padding',
        children=html.Div([
           html.Div(html.Div(TEXT['no_data_selected'], className='dao-info-name'), id=org_id+'-info'),
           _get_dao_summary_layout(org_id, datapoints)
        ], className='dao-header-container'),
    )

def __generate_sections(sections: Dict[str, List[Callable]]) -> html.Div:
    tabs: List[dcc.Tab] = []

    for name, data in sections.items():
        charts = list()
        for chart_pane in data['callables']:
            charts.append(chart_pane())
        
        sec = html.Div(
            className='flex-column small-padding',
            children=[
                html.Div(name, id=data['css_id'], className='section-title section-left-padding-aligner'),
                html.Div(children=charts, className='flex-row flex-wrap flex-align-start')
            ],
        )

        tabs.append(dcc.Tab(label=name, children=[
            sec
        ]))

    return html.Div(dcc.Tabs(tabs), className='flex-column body')
