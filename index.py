"""
   Descp: It's used as entry point on the web app. It also configures some
          settings, such as routes.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os

from dash import dcc
from dash import html

from src.app import app, DEBUG
from src.matomo import Matomo
import src.apps.common.resources.colors as COLOR
from src.apps.common.resources.strings import TEXT
from src.apps.common.presentation.main_view.main_view_controller import bind_callbacks

import pandas as pd
pd.options.mode.chained_assignment = 'warn' if DEBUG else None

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
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

app.index_string = index_string
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Loading(
        type="circle",
        color=COLOR.DARK_BLUE,
        fullscreen=True,
        children=html.Div(id='header-loading-state', className='display-none')),
    html.Div(id='current-platform', hidden=True)
])

bind_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=DEBUG, dev_tools_ui=DEBUG)
