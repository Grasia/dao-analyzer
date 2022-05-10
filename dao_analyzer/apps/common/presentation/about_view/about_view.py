"""
   Descp: Common elements of the view.

   Created on: 1-apr-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from pathlib import Path

from dash import html, dcc
import dash_bootstrap_components as dbc

ABOUT_MD = Path('./ABOUT.md')

def get_layout() -> html.Div:
    return dbc.Container(__get_body(), className='top-body p-5')

def __get_body() -> html.P:
    with open(ABOUT_MD, 'r') as mdf:
        return dcc.Markdown(mdf.read(), className='markdown')