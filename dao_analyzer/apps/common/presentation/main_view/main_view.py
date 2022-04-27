"""
   Descp: Common elements of the view.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os
from dash import html

from dao_analyzer import __version__
from dao_analyzer.apps.common.resources.strings import TEXT

REL_PATH: str = os.path.join('..', '..', '..', '..', 'assets')


def generate_layout(body: html.Div) -> html.Div:

    return html.Div(children=[
        __generate_header(),
        body,
        __generate_foot(),
    ], className='root',)


def __generate_header() -> html.Div:
    return html.Div(children=[
        #html.Img(src=os.path.join(REL_PATH, TEXT['dao_analyzer_header_name']), className='header-back-img'),
        html.Img(src=os.path.join(REL_PATH, TEXT['dao_analyzer_logo_name']), className='header-logo'),
    ], className='main-header')


def __generate_foot() -> html.Div:
    return html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Span(TEXT['current_version'].format(version=__version__), className='small-text-aligner'),
                html.Img(src=os.path.join(REL_PATH, TEXT['github_icon_name']), className='github-logo'),
                html.Span(TEXT['follow_us'], className='small-text-aligner'),
                html.A(TEXT['github'], href=TEXT['github_url'],
                    target='_blank', className='url-color')
            ], className='flex-row'),

            html.Div(children=[

                html.Div(children=[
                    html.A(children=[
                        html.Img(src=os.path.join(REL_PATH, TEXT['cc_image_name']), className='license-img'),
                    ], href=TEXT['cc_url'], target='_blank'),
                    html.A(children=[
                        html.Img(src=os.path.join(REL_PATH, TEXT['gpl_image_name']), className='license-img'),
                    ], href=TEXT['gpl_url'], target='_blank'),
                ], className='foot-ack-logos flex-column'),

                html.Div(children=[
                    html.P(children=[
                            f"{TEXT['cc_license_text']}. {TEXT['gpl_license_text']}. ",
                            html.A(TEXT['p2p_models'], href=TEXT['p2p_models_url'], target='_blank', className='url-color'),
                            f"{TEXT['acknowledgements']}."
                        ],
                        className=''),
                ], className=''),
            ], className='flex-row')

        ], className='foot-left flex-column'),

        html.Div(children=[
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
        ], className='flex-row foot-left-aligner')

    ], className='main-foot left-padding-aligner right-padding-aligner')