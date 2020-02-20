"""
   app.py

   Descp: Used to wrap the dash instance

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import dash

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True