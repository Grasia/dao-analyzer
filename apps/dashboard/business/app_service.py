"""
   Descp: Manage the application logic, and it's used to interconect the 
          data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
import dash_html_components as html

from apps.dashboard.presentation.layout import generate_layout
from apps.dashboard.data_access.daos.dao_organization import get_all_orgs
from apps.dashboard.data_access.daos.dao_new_user_metric import get_new_users_metric
import apps.dashboard.business.transfers as tr
from apps.dashboard.business.service_state import ServiceState

state: ServiceState = None


def __get_state():
    global state
    if not state:
        state = ServiceState()
    return state


def get_layout() -> html.Div:
    """
    Returns the app's view. 
    """
    orgs: List[tr.Organization] = get_all_orgs()
    labels: List[Dict[str, str]] = \
        [{'value': o.id, 'label': o.name} for o in orgs]

    __get_state().set_orgs_ids([o.id for o in orgs])
    return generate_layout(labels)


def get_metric_new_users(ids: List[str]) -> tr.MetricTimeSeries:
    return get_new_users_metric(ids)