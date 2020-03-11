"""
   Descp: Manage the application logic, and it's used to interconect the
        data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
import dash_html_components as html

import src.apps.daostack.presentation.layout as ly
from src.apps.daostack.data_access.dao_organization import get_all_orgs
import src.apps.daostack.data_access.dao_stacked_serie as s_dao
import src.apps.daostack.data_access.dao_proposal_outcome_serie as prop_dao
from src.apps.daostack.business.transfers.organization import Organization
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.resources.strings import TEXT


__service = None

def get_service():
    """
    Singelton object.
    """
    global __service
    if not __service:
        __service = Service()
    return __service


class Service():
    __ALL_ORGS_ID: str = '1'


    def __init__(self, dao_org = None, dao_serie = None, dao_prop = None):
        # Dao's callers
        self.__dao_org = dao_org if dao_org else get_all_orgs
        self.__dao_serie = dao_serie if dao_serie else s_dao.get_metric
        self.__dao_prop = dao_prop if dao_prop else prop_dao.get_metric

        # app state
        self.__org_ids = list()


    def get_ids(self) -> List[str]:
        return self.__org_ids


    def get_layout(self) -> html.Div:
        """
        Returns the app's view. 
        """
        # request orgs names
        orgs: List[Organization] = self.__dao_org()
        labels: List[Dict[str, str]] = list()

        if orgs:
            [{'value': o.id, 'label': o.name} for o in orgs]

            labels = sorted(labels, key = lambda k: k['label'])

            # add all orgs selector
            labels = [{'value': self.__ALL_ORGS_ID, 'label': TEXT['all_orgs']}]\
                + labels
            # add them to the app's state
            self.__org_ids = [o.id for o in orgs]

        return ly.generate_layout(labels)


    def __get_ids_from_id(self, _id: str) -> List[str]:
        """
        Gets a list of ids from a _id attr.
        If _id is equals to 'all orgs' id then returns a list with all the orgs id.
        If not returns a list with _id as unique element of the list.
        """
        if _id == self.__ALL_ORGS_ID:
            return self.__org_ids
        else:
            return [_id]


    def get_metric_new_users(self, d_id: str) -> StackedSerie:
        return self.__dao_serie(ids = self.__get_ids_from_id(d_id), 
            m_type = s_dao.METRIC_TYPE_NEW_USERS)


    def get_metric_new_proposals(self, d_id: str) -> StackedSerie:
        return self.__dao_serie(ids = self.__get_ids_from_id(d_id), 
            m_type = s_dao.METRIC_TYPE_NEW_PROPOSAL)


    def get_metric_type_proposals(self, d_id: str) -> Dict:
        metric: StackedSerie = self.__dao_prop(ids = self.__get_ids_from_id(d_id))
        text: List[str] = [TEXT['abs_pass'],
                        TEXT['rel_pass'],
                        TEXT['rel_fail'],
                        TEXT['abs_fail']]
        color: List[str] = [ly.DARK_GREEN,
                            ly.LIGHT_GREEN,
                            ly.LIGHT_RED,
                            ly.DARK_RED]

        return {'metric': metric, 'text': text, 'color': color}
