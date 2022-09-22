"""
   Descp: Common elements of the view.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os
from dash import html
import dash_bootstrap_components as dbc

from dao_analyzer.web import __version__
from dao_analyzer.web.apps.common.resources.strings import TEXT

REL_PATH: str = os.path.join('..', '..', '..', '..', 'assets')


def generate_layout(body: html.Div) -> html.Div:

    return html.Div(children=[
        __generate_header(),
        body,
        __generate_foot(),
    ], className='root',)


def __generate_header() -> html.Div:
    return html.Div(children=[
        html.Div([
            html.Img(src=os.path.join(REL_PATH, TEXT['dao_analyzer_logo_name']), className='header-logo'),
            html.Span(TEXT['dao_analyzer_header_text'], className='header-text'),
        ], className='header-things-container'),
        dbc.Container([
            html.A('About', href="/about", className="header-link"),
        ], className='header-links-container'),
    ], className='main-header')


def __generate_foot() -> html.Div:
    return html.Footer(
        dbc.Container(children=[
            dbc.Row([
                html.Div([
                    html.I(className='bi bi-github'),
                    ' ',
                    TEXT['follow_us'],
                    html.A(TEXT['github'], href=TEXT['github_url'], target='_black', className='url-color')
                ], className='col'),
                html.Div(TEXT['current_version'].format(version=__version__), className='col-12 col-sm text-sm-end'),
            ], className='mb-3'),
            dbc.Row([
                html.Div([
                    html.Div(children=[
                        html.A(children=[
                            html.Img(src=os.path.join(REL_PATH, TEXT['cc_image_name']), className='license-img'),
                        ], href=TEXT['cc_url'], target='_blank'),
                        html.A(children=[
                            html.Img(src=os.path.join(REL_PATH, TEXT['gpl_image_name']), className='license-img'),
                        ], href=TEXT['gpl_url'], target='_blank'),
                    ], className='foot-ack-logos'),
                    html.Div(children=[
                        html.P([
                            f"{TEXT['cc_license_text']}. {TEXT['gpl_license_text']}. ",
                            html.A(TEXT['p2p_models'], href=TEXT['p2p_models_url'], target='_blank', className='url-color'),
                            f"{TEXT['acknowledgements']}."
                        ]),
                    ]),
                ], className='col d-flex flex-row'),
                html.Div([
                    html.A(children=[
                        html.Img(src=os.path.join(REL_PATH, TEXT['spanish_ministry_image_name']),
                            className='sponsor-img'),
                    ], href=TEXT['spanish_ministry_url'], target='_blank'),
                    html.A(children=[
                        html.Img(src=os.path.join(REL_PATH, TEXT['logo_ucm_name']),
                            className='sponsor-img'),
                    ], href=TEXT['ucm_url'], target='_blank'),
                    html.A(children=[
                        html.Img(src=os.path.join(REL_PATH, TEXT['logo_grasia_name']),
                            className='sponsor-img'),
                    ], href=TEXT['grasia_url'], target='_blank'),
                    html.A(children=[
                        html.Img(src=os.path.join(REL_PATH, TEXT['erc_image_name']),
                            className='sponsor-img'),
                    ], href=TEXT['erc_url'], target='_blank'),
                ], className='col footer-logos-container'),
            ], className='row-cols-1 row-cols-lg-2 gy-3'),
        ]), className='mt-3'
    )
