"""
   Descp: Used to wrap the dash instance

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import os
import dash

DEBUG = os.environ['DEBUG'] == 'TRUE' if 'DEBUG' in os.environ else False

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True