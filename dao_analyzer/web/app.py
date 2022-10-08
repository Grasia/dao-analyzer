"""
   Descp: Used to wrap the dash instance

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import argparse
import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

import pandas as pd

from .matomo import Matomo
from .apps.common.resources import colors as COLOR
from .apps.common.resources.strings import TEXT
from .apps.common.presentation.main_view.main_view_controller import bind_callbacks

DEBUG = 'DEBUG' in os.environ and os.environ['DEBUG'].lower() == 'true' or \
        'FLASK_ENV' in os.environ and os.environ['FLASK_ENV'].lower() == 'development'

pd.options.mode.chained_assignment = 'warn' if DEBUG else None

app = dash.Dash(__name__, 
    suppress_callback_exceptions=True, 
    external_scripts=[
    ],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
    ],
    meta_tags=[
        { 'name': 'viewport', 'content': 'width=device-width, initial-scale=1' },
    ],
)

if DEBUG:
    pd.options.mode.chained_assignment = None # 'warn' TODO: Delete none
    app.enable_dev_tools(
        debug=True,
    )

matomo_url = None
site_id = None
if 'DAOA_MATOMO_URL' in os.environ:
    matomo_url = os.environ['DAOA_MATOMO_URL']
    site_id = int(os.environ['DAOA_MATOMO_SITE_ID'])

    if matomo_url[-1] != '/': 
        matomo_url += '/'

server = app.server

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.title = TEXT['app_title']
index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
    '''

if matomo_url:
    index_string += Matomo(matomo_url, site_id).get_script()

index_string += '''
        </head>
        <body>
            {%app_entry%}
            {%config%}
            {%scripts%}
            {%renderer%}
        </body>
    </html>
    '''

app.index_string = index_string
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Loading(
        type="cube",
        color=COLOR.DARK_BLUE,
        fullscreen=True,
        children=html.Div(id='header-loading-state', className='d-none')),
])

bind_callbacks(app)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host',
        help='Host IP used to serve the application',
        default=os.getenv('HOST', '127.0.0.1'),
    )
    parser.add_argument(
        '-P', '--port',
        help='Port used to serve the application',
        default=os.getenv('PORT', 8050),
    )

    args = parser.parse_args()
    
    app.run_server(
        debug=DEBUG, 
        dev_tools_ui=DEBUG,
        host=args.host,
        port=args.port,
    )
