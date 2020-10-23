"""
   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Callable
import dash_core_components as dcc
import dash_html_components as html

from src.apps.common.resources.strings import TEXT


def generate_layout(labels: List[Dict[str, str]], sections: Dict, color_app: str) -> List:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    return [__generate_selector(labels), __generate_sections(sections, color_app)]
    

def __generate_selector(labels: List[Dict[str, str]]) -> html.Div:
    return html.Div( 
        children = [
            html.Span(TEXT['dao_selector_title']),
            dcc.Dropdown(
                id='org-dropdown',
                options=labels,
                className='drop-down'
            )
        ],
        className='dao-selector-pane',
    )


def __generate_sections(sections: Dict[str, List[Callable]], color_app: str) -> html.Div:
    children: List = list()

    for name, data in sections.items():
        charts = list()
        for chart_pane in data['callables']:
            charts.append(chart_pane())
        
        sec = html.Div(
            className='section',
            children=[
                html.Div(name, id=data['css_id'], className=f'title-section {color_app}'),
                html.Div(children=charts, className='graph-section')
            ],
        )
        children.append(sec)

    return html.Div(children=children)
