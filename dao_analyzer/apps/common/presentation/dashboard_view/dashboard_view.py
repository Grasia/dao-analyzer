"""
   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os
from typing import Dict, List, Callable
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

def generate_layout(labels: List[Dict[str, str]], sections: Dict, ecosystem: str, update: str, org_id: str, org_value: str) -> List:
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
        __generate_subheader(org_id),
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

def __generate_subheader(org_id: str) -> html.Div:
    return html.Div(
        id=org_id,
        className='flex-column body small-padding dao-info',
        children=html.Div(TEXT['no_data_selected'], className='dao-info-name'))


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
