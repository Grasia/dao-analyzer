"""
   Descp: Manage the application logic, and it's used to interconect the
        data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Any
import dash_html_components as html

import src.apps.daostack.presentation.layout as ly
from src.apps.daostack.data_access.graphql.dao_organization import DaoOrganizationList
import src.apps.daostack.data_access.graphql.dao_metric.\
    dao_metric_factory as s_factory
from src.api.graphql.daostack.api_manager import ApiRequester
from src.apps.daostack.business.transfers.organization import OrganizationList
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.n_stacked_serie import NStackedSerie
from src.apps.daostack.resources.strings import TEXT
import src.apps.daostack.resources.colors as Color


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
    __DATE_FORMAT: str = '%b, %Y'


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


    def __get_sserie_by_metric(self, metric: int, o_id: str) -> Any:
        dao = s_factory.get_dao(
            ids=self.__orgs.get_ids_from_id(o_id),
            metric=metric)

        return dao.get_metric()


    def __get_common_representation(self, metric: StackedSerie, 
    complements: bool = True) -> Dict:

        y: List[float] = metric.get_i_stack(0)
        color = [Color.LIGHT_BLUE] * len(y)
        if color:
            color[-1] = Color.DARK_BLUE

        data: Dict = {
            'serie': {
                'y': y,
                'color': color,
                'name': '',
            },
            'common': {
                'x': metric.get_serie(),
                'type': 'date',
                'x_format': self.__DATE_FORMAT,
                'ordered_keys': ['serie'],
            }
        }

        if complements:
            data['common']['last_serie_elem'] = metric.get_last_serie_elem()
            data['common']['last_value'] = metric.get_last_value(0)
            data['common']['diff'] = metric.get_diff_last_values(0)

        return data


    def get_metric_new_users(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.NEW_USERS, o_id)

        return self.__get_common_representation(metric=metric)


    def get_metric_different_voters(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.DIFFERENT_VOTERS, o_id)

        return self.__get_common_representation(metric=metric)


    def get_metric_different_stakers(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.DIFFERENT_STAKERS, o_id)

        return self.__get_common_representation(metric=metric)


    def get_metric_new_proposals(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.NEW_PROPOSALS, o_id)
        
        return self.__get_common_representation(metric=metric)


    def get_metric_proposal_boost_outcome(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.PROPOSALS_BOOST_OUTCOME, o_id)

        y1 = metric.get_i_stack(0)
        y2 = metric.get_i_stack(1)
        y3 = metric.get_i_stack(2)
        y4 = metric.get_i_stack(3)
        data: Dict = {
            'serie1': {
                'y': y1,
                'color': [Color.DARK_GREEN]*len(y1),
                'name': TEXT['queue_pass'],
            },
            'serie2': {
                'y': y2,
                'color': [Color.LIGHT_GREEN]*len(y2),
                'name': TEXT['boost_pass'],
            },
            'serie3': {
                'y': y3,
                'color': [Color.LIGHT_RED]*len(y3),
                'name': TEXT['boost_fail'],
            },
            'serie4': {
                'y': y4,
                'color': [Color.DARK_RED]*len(y4),
                'name': TEXT['queue_fail'],
            },
            'common': {
                'x': metric.get_serie(),
                'type': 'date',
                'x_format': self.__DATE_FORMAT,
                'ordered_keys': ['serie1', 'serie2', 'serie3', 'serie4'],
            },
        }
        return data


    def get_metric_total_votes(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.TOTAL_VOTES, o_id)

        return self.__get_common_representation(metric=metric)


    def get_metric_total_stakes(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.TOTAL_STAKES, o_id)

        return self.__get_common_representation(metric=metric)


    def get_metric_proposal_majority(self, o_id: str) -> Dict:
        metric: NStackedSerie = self.__get_sserie_by_metric(
            s_factory.PROPOSAL_MAJORITY, o_id)

        y1: StackedSerie = metric.get_i_sserie(0)
        y2: StackedSerie = metric.get_i_sserie(1)
        y3: StackedSerie = metric.get_i_sserie(2)
        y4: StackedSerie = metric.get_i_sserie(3)
        x: List = y1.get_serie()

        data: Dict = {
            'serie1': {
                'x': y1.get_serie(),
                'y': y1.get_i_stack(0),
                'color': f'rgba{Color.hex_to_rgba(Color.DARK_GREEN, 0.5)}',
                'marker_symbol': 'triangle-up',
                'name': TEXT['abs_pass'],
                'position': 'up',
            },
            'serie2': {
                'x': y2.get_serie(),
                'y': y2.get_i_stack(0),
                'color': f'rgba{Color.hex_to_rgba(Color.DARK_GREEN, 0.5)}',
                'marker_symbol': 'circle',
                'name': TEXT['rel_pass'],
                'position': 'up',
            },
            'serie3': {
                'x': y3.get_serie(),
                'y': y3.get_i_stack(0),
                'color': f'rgba{Color.hex_to_rgba(Color.DARK_RED, 0.5)}',
                'marker_symbol': 'circle',
                'name': TEXT['rel_fail'],
                'position': 'down',
            },
            'serie4': {
                'x': y4.get_serie(),
                'y': y4.get_i_stack(0),
                'color': f'rgba{Color.hex_to_rgba(Color.DARK_RED, 0.5)}',
                'marker_symbol': 'triangle-down',
                'name': TEXT['abs_fail'],
                'position': 'down',
            },
            'common': {
                'x': x,
                'type': 'date', 
                'x_format': self.__DATE_FORMAT,
                'ordered_keys': ['serie1', 'serie2', 'serie3', 'serie4'], 
                'y_suffix': '%',
            }
        }

        return data 


    def get_metric_prop_total_succes_ratio(self, o_id: str) -> Dict:
        metric: StackedSerie = self.__get_sserie_by_metric(
            s_factory.PROPOSALS_TOTAL_SUCCES_RATIO, o_id)

        return self.__get_common_representation(metric=metric, complements=False)


    def get_metric_prop_boost_succes_ratio(self, o_id: str) -> Dict:
        metric: NStackedSerie = self.__get_sserie_by_metric(
            s_factory.PROPOSALS_BOOST_SUCCES_RATIO, o_id)

        y1 = metric.get_i_sserie(0).get_i_stack(0)
        y2 = metric.get_i_sserie(1).get_i_stack(0)

        data: Dict = {
            'serie1': {
                'y': y1,
                'color': [Color.LIGHT_GREEN]*len(y1),
                'name': TEXT['boost'],
            },
            'serie2': {
                'y': y2,
                'color': [Color.DARK_RED]*len(y2),
                'name': TEXT['not_boost'],
            },
            'common': {
                'x': metric.get_serie(),
                'type': 'date',
                'x_format': self.__DATE_FORMAT,
                'ordered_keys': ['serie1', 'serie2'],
            }
        }

        return data
