"""
   Descp: Common elements of the view.

   Created on: 1-apr-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
import pkgutil

from dash import html, dcc
import dash_bootstrap_components as dbc

from ...... import web

ABOUT_MD = pkgutil.get_data(web.__name__, 'assets/ABOUT.md').decode('utf-8')

def get_layout() -> html.Div:
    return dbc.Container(__get_body(), className='top body py-5')

def __get_body() -> html.Div:
    # with open(ABOUT_MD, 'r') as mdf:
    md = dcc.Markdown(ABOUT_MD, className='markdown mt-3')

    back = html.A('Back', href='/', className='about-back')

    return html.Div([back, md], className='col-md-6 mx-auto')