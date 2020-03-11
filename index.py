"""
   Descp: It's used as entry point on the web app. It also configures some
          settings, such as routes.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from src.app import app, DEBUG
import src.apps.daostack.business.app_service as service
import src.apps.daostack.presentation.controller as controller


# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/dashboard':
        controller.init()
        return service.get_layout()
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=DEBUG, dev_tools_ui=DEBUG)
