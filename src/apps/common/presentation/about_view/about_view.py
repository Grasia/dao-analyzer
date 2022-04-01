"""
   Descp: Common elements of the view.

   Created on: 1-apr-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from pathlib import Path

from dash import html
from dash import dcc

ABOUT_MD = Path('./ABOUT.md')

def get_layout() -> html.Div:
    return html.Div(children=[
        html.Div(__get_body(), className='flex-column body')
    ], className='main-body left-padding-aligner right-padding-aligner')

def __get_body() -> html.P:
    with open(ABOUT_MD, 'r') as mdf:
        return dcc.Markdown(mdf.read(), className='flex-column medium-padding markdown')