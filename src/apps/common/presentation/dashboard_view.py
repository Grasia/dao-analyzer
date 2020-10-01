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


def generate_layout(labels: List[Dict[str, str]], sections: Dict) -> html.Div:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    return html.Div(
        children=[
            html.Div(
                children=[__generate_header()],
                className='main-header fix-height'
            ),

            html.Div(
                children=[
                    __generate_selector(labels),
                    __generate_sections(sections)
                ],
                className='main-body'
            ),

            html.Div(
                children=[__generate_foot()],
                className='main-foot'
            ),
        ],
        className='root',
    )


def __generate_header() -> html.H1:
    return html.H1(TEXT['app_title'])
    

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


def __generate_sections(sections: Dict[str, List[Callable]]) -> html.Div:
    children: List = list()

    for name, callables in sections.items():
        charts = list()
        for chart_pane in callables:
            charts.append(chart_pane())
        
        sec = html.Div(
            className='section',
            children=[
                html.Div(name, className='title-section'),
                html.Div(children=charts, className='graph-section')
            ],
        )
        children.append(sec)

    return html.Div(children=children)


def __generate_foot() -> html.Div:
    return html.Div(children=[
                    html.Div(children=[
                        html.Span(TEXT['github'], className='right-separator bold'),
                        html.A(TEXT['github_url'], href=TEXT['github_url'], target='_blank')
                    ], className='center-aligner medium-font small-vertical-margin'),
                    html.Div(children=[
                        html.Div(children=[
                            html.A(children=[
                                html.Img(src=TEXT['cc_image_url'], className='license-img'),
                            ], href=TEXT['cc_url'], target='_blank'),
                            html.A(children=[
                                html.Img(src=TEXT['gpl_image_url'], className='license-img'),
                            ], href=TEXT['gpl_url'], target='_blank'),
                        ], className='column-container padding-30 center-aligner medium-horizontal-margin'),
                        html.Div(children=[
                            html.P(children=[
                                    f"{TEXT['cc_license_text']}. {TEXT['gpl_license_text']}. ",
                                    html.A(TEXT['p2p_models'], href=TEXT['p2p_models_url'], target='_blank'),
                                    f"{TEXT['acknowledgements']}."
                                ],
                                className='small-font'),
                        ], className='padding-30 medium-horizontal-margin'),
                        html.Div(children=[
                            html.A(children=[
                                html.Img(src=TEXT['erc_image_url'], className='sponsor-img'),
                            ], href=TEXT['erc_url'], target='_blank'),
                            html.A(children=[
                                html.Img(src=TEXT['spanish_ministry_image_url'], className='sponsor-img'),
                            ], href=TEXT['spanish_ministry_url'], target='_blank')
                        ], className='column-container padding-30 center-aligner medium-horizontal-margin')
                    ], className='row-container medium-bottom-margin center-aligner space-aligner')
                ])
