"""
   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os
from typing import Dict, List, Callable
import dash_core_components as dcc
import dash_html_components as html

from src.apps.common.resources.strings import TEXT
from src.apps.common.presentation.main_view.main_view import REL_PATH

__ECOSYSTEM_SELECTED: Dict[str, List[str]] = {
    'default': ['', '', ''],
    'daostack': ['daostack-selected', '', ''],
    'aragon': ['', 'aragon-selected', ''],
    'daohaus': ['', '', 'daohaus-selected'],
}

def generate_layout(labels: List[Dict[str, str]], sections: Dict, ecosystem: str) -> List:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    return html.Div(children=[
        __generate_header(labels, ecosystem),
        #__generate_sections(sections)
    ], className='main-body left-padding-aligner right-padding-aligner')
    

def __generate_header(labels: List[Dict[str, str]], ecosystem: str) -> html.Div:
    selected: List[str] = __ECOSYSTEM_SELECTED['default']
    if ecosystem in __ECOSYSTEM_SELECTED.keys():
        selected = __ECOSYSTEM_SELECTED[ecosystem]

    return html.Div(children=[
        html.Div(children=[
            html.Span(TEXT['ecosystem_selector_title']),
            html.Div(children=[
                html.Div(children=[
                    html.Div(className='ecosystem-overlay ecosystem daostack-color',
                        id='daostack-bt'),
                    html.Img(src=os.path.join(REL_PATH, TEXT['daostack_image_name']),
                        className='ecosystem-img flex-size-1'),
                ], className=f'ecosystem daostack-ecosystem {selected[0]}'),
                html.Div(children=[
                    html.Div(className='ecosystem-overlay ecosystem aragon-color', 
                        id='aragon-bt'),
                    html.Img(src=os.path.join(REL_PATH, TEXT['aragon_image_name']),
                        className='ecosystem-img flex-size-1'),
                ], className=f'ecosystem aragon-ecosystem {selected[1]}'),
                html.Div(children=[
                    html.Div(className='ecosystem-overlay ecosystem daohaus-color',
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
                className='flex-size-3',
            )
        ], className='flex-row flex-size-1'),

    ], className='body-header small-padding flex-row')


def __generate_sections(sections: Dict[str, List[Callable]]) -> html.Div:
    children: List = list()

    for name, data in sections.items():
        charts = list()
        for chart_pane in data['callables']:
            charts.append(chart_pane())
        
        sec = html.Div(
            className='section',
            children=[
                html.Div(name, id=data['css_id'], className=''),
                html.Div(children=charts, className='graph-section')
            ],
        )
        children.append(sec)

    return html.Div(children=children)
