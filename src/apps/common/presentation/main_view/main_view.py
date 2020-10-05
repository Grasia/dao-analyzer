"""
   Descp: Main view where to select the DAO ecosystem.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import dash_html_components as html

from src.apps.common.resources.strings import TEXT

REL_PATH: str = '../../../../assets/'


def generate_layout(body: html.Div = None) -> html.Div:
    if not body:
        body = __generate_body()

    return html.Div(children=[
        html.Div(
            children=[__generate_header()],
            className='main-header fix-height'
        ),
        html.Div(
            children=body,
            className='main-body',
        ),
        html.Div(
            children=[],
            className='main-foot',
        ),
    ], className='root',)


def __generate_header() -> html.H1:
    return html.H1(TEXT['app_title'])


def __generate_body() -> html.Div:
    return html.Div(children=[
        html.Div(children=[
            __generate_ecosystem_pane(
                img=f'{REL_PATH}daostack.png',
                title=TEXT['daostack'],
                bt_id='daostack-bt'),
            __generate_ecosystem_pane(
                img=f'{REL_PATH}daohaus.png',
                title=TEXT['daohaus'],
                bt_id='daohaus-bt'),
        ], 
        className='eco-body '),
        html.Div(className='page-filler')
    ], 
    className='')


def __generate_ecosystem_pane(img: str, title: str, bt_id: str) -> html.Div:
    return html.Div(children=[
        html.Div(children=[
            html.H2(title, className=''),
            html.Span(TEXT['ecosystem'], className=''), 
        ]),
        html.Img(src=img, className='eco-img'),
        html.Button(TEXT['bt_analyze'], id=bt_id, n_clicks=0),
    ], 
    className='eco-pane ')


def generate_foot() -> html.Div:
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