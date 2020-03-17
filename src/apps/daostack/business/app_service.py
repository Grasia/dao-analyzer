"""
   Descp: Manage the application logic, and it's used to interconect the
        data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List
import dash_html_components as html

import src.apps.daostack.presentation.layout as ly
from src.apps.daostack.data_access.graphql.dao_organization import DaoOrganizationList
import src.apps.daostack.data_access.graphql.dao_stacked_serie.\
    dao_stacked_serie_factory as s_factory
from src.api.graphql.daostack.api_manager import ApiRequester
from src.apps.daostack.business.transfers.organization import OrganizationList
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
    def __init__(self):
        # app state
        self.__orgs: OrganizationList = None


    def get_organizations(self) -> OrganizationList:
        if not self.__orgs:
            orgs: OrganizationList = DaoOrganizationList(ApiRequester())\
                .get_organizations()
            if not orgs.is_empty():
                self.__orgs = orgs
                
        return self.__orgs


    def get_layout(self) -> html.Div:
        """
        Returns the app's view. 
        """
        orgs: OrganizationList = self.get_organizations()
        return ly.generate_layout(orgs.get_dict_representation())


    def __get_sserie_by_metric(self, metric: int, o_id: str) -> StackedSerie:
        dao = s_factory.get_dao(
            ids=self.__orgs.get_ids_from_id(o_id),
            metric=metric)

        return dao.get_stacked_serie()


    def get_metric_new_users(self, o_id: str) -> StackedSerie:
        return self.__get_sserie_by_metric(s_factory.NEW_USERS, o_id)


    def get_metric_different_voters(self, o_id: str) -> StackedSerie:
        return self.__get_sserie_by_metric(s_factory.DIFFERENT_VOTERS, o_id)


    def get_metric_different_stakers(self, o_id: str) -> StackedSerie:
        return self.__get_sserie_by_metric(s_factory.DIFFERENT_STAKERS, o_id)


    def get_metric_new_proposals(self, o_id: str) -> StackedSerie:
        return self.__get_sserie_by_metric(s_factory.NEW_PROPOSALS, o_id)


    def get_metric_proposal_boost_outcome(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.PROPOSALS_BOOST_OUTCOME, o_id)
            
        text: List[str] = [TEXT['queue_pass'],
                        TEXT['boost_pass'],
                        TEXT['boost_fail'],
                        TEXT['queue_fail']]
        color: List[str] = [ly.DARK_GREEN,
                            ly.LIGHT_GREEN,
                            ly.LIGHT_RED,
                            ly.DARK_RED]

        return {'metric': metric, 'text': text, 'color': color}


    def get_metric_total_votes(self, o_id: str) -> StackedSerie:
        return self.__get_sserie_by_metric(s_factory.TOTAL_VOTES, o_id)


    def get_metric_total_stakes(self, o_id: str) -> StackedSerie:
        return self.__get_sserie_by_metric(s_factory.TOTAL_STAKES, o_id)
