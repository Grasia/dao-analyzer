"""
   Descp: Used to wrap the dash instance

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import os
import dash

DEBUG = 'DEBUG' in os.environ and os.environ['DEBUG'].lower() == 'true' or \
        'FLASK_ENV' in os.environ and os.environ['FLASK_ENV'].lower() == 'development'

app = dash.Dash(__name__, suppress_callback_exceptions=True)
