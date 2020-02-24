"""
   controller.py

   Descp: It's used to manage the dashboard events.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict

from dash.dependencies import Input, Output
import dash_html_components as html

from app import app
from apps.dashboard.daos.dao import get_all_daos
from apps.dashboard.layout import generate_layout


def get_layout() -> html.Div:
    daos: List[Dict[str, str]] = get_all_daos()
    labels: List[Dict[str, str]] = [{'value': obj['id'], 
        'label': obj['name']} for obj in daos]

    return generate_layout(labels)