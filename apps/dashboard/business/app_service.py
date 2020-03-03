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
from apps.dashboard.data_access.dao_organization import get_all_orgs
from apps.dashboard.data_access.dao_metric_time_series import get_metric
import apps.dashboard.business.transfers as tr
from apps.dashboard.business.service_state import ServiceState
from apps.dashboard.presentation.strings import TEXT

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
    # request orgs names
    orgs: List[tr.Organization] = get_all_orgs()
    labels: List[Dict[str, str]] = \
        [{'value': o.id, 'label': o.name} for o in orgs]

    labels = sorted(labels, key = lambda k: k['label'])

    # add all orgs selector
    labels = [{'value': __get_state().ALL_ORGS_ID, 'label': TEXT['all_orgs']}]\
             + labels
    # add them to the app's state
    __get_state().set_orgs_ids([o.id for o in orgs])

    return generate_layout(labels)


def __get_ids_from_id(_id: str) -> List[str]:
    """
    Gets a list of ids from a _id attr.
    If _id is equals to 'all orgs' id then returns a list with all the orgs id.
    If not returns a list with _id as unique element of the list.
    """
    if _id == __get_state().ALL_ORGS_ID:
        return __get_state().organization_ids
    else:
        return [_id]


def get_metric_new_users(d_id: str) -> tr.MetricTimeSeries:
    return get_metric(ids = __get_ids_from_id(d_id), 
        o_type = tr.MetricTimeSeries.METRIC_TYPE_NEW_USERS)


def get_metric_new_proposals(d_id: str) -> tr.MetricTimeSeries:
    return get_metric(ids = __get_ids_from_id(d_id), 
        o_type = tr.MetricTimeSeries.METRIC_TYPE_NEW_PROPOSAL)