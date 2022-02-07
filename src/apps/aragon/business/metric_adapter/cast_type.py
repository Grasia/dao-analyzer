"""
   Descp: Class to adapt StakedSeries in a chart. This class is used to adapt
          the 'votes by type' metric

   Created on: 21-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, Callable

import src.apps.common.resources.colors as Color
from src.apps.aragon.resources.strings import TEXT
from src.apps.common.business.transfers.stacked_serie import StackedSerie
from src.apps.common.business.transfers.organization import OrganizationList
from src.apps.common.business.i_metric_adapter import IMetricAdapter
import src.apps.aragon.data_access.daos.metric.\
    metric_dao_factory as s_factory

class CastType(IMetricAdapter):

    DATE_FORMAT: str = '%b, %Y'

    def __init__(self, organizations: Callable[...,OrganizationList]) -> None:
        self.__organizations = organizations


    @property
    def organizations(self) -> OrganizationList:
        return self.__organizations()


    def get_plot_data(self, o_id: str) -> Dict:
        """
        Returns the metric data in a Dict using o_id param.
        """
        dao = s_factory.get_dao(
            ids=self.organizations.get_ids_from_id(o_id),
            metric=s_factory.CAST_TYPE
        )
        metric: StackedSerie = dao.get_metric()

        last_value: int = metric.get_last_value(0) + metric.get_last_value(1)
        diff: float = metric.get_diff_last_values(add_stacks=True)

        return {
            'type1': {
                'y': metric.get_i_stack(0),
                'color': Color.LIGHT_RED,
                'name': TEXT['votes_against'],
            },
            'type2': {
                'y': metric.get_i_stack(1),
                'color': Color.LIGHT_GREEN,
                'name': TEXT['votes_for'],
            },
            'common': {
                'x': metric.get_serie(),
                'type': 'date',
                'x_format': self.DATE_FORMAT,
                'ordered_keys': ['type1', 'type2'],
            },
            'last_serie_elem': metric.get_last_serie_elem(),
            'last_value': last_value,
            'diff': diff, 
        }
