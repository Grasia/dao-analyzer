"""
   Descp: This class is used to adapt the vote and stake type
          metric to its visual representation.

   Created on: 14-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict
from dao_analyzer.web.apps.common.business.transfers.organization.organization_list import OrganizationList

import dao_analyzer.web.apps.common.resources.colors as Color
from dao_analyzer.web.apps.daostack.resources.strings import TEXT
from dao_analyzer.web.apps.daostack.business.metric_adapter.metric_adapter import MetricAdapter
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
import dao_analyzer.web.apps.daostack.data_access.daos.metric.\
    metric_dao_factory as s_factory

class VoteType(MetricAdapter):
    VOTE: int = 0
    STAKE: int = 1

    def __init__(self, metric_id: int, mtype: int) -> None:
        super().__init__(metric_id)
        self.__mtype: int = self.__get_type(mtype)


    def __get_type(self, mtype: int) -> int:
        t: int = mtype
        if t not in [VoteType.VOTE, VoteType.STAKE]:
            t = VoteType.VOTE
        return t

    
    def get_plot_data(self, o_id: str, organizations: OrganizationList) -> Dict:
        """
        Returns the metric data in a Dict using o_id param.
        """
        dao = s_factory.get_dao(
            ids=organizations.get_ids_from_id(o_id),
            metric=super().metric_id
        )
        metric: StackedSerie = dao.get_metric()

        last_value: int = metric.get_last_value(0) + metric.get_last_value(1)

        return {
            'type1': {
                'y': metric.get_i_stack(0),
                'color': Color.LIGHT_RED,
                'name': TEXT['votes_against'] if self.__mtype is self.VOTE
                    else TEXT['downstakes'],
            },
            'type2': {
                'y': metric.get_i_stack(1),
                'color': Color.LIGHT_GREEN,
                'name': TEXT['votes_for']if self.__mtype is self.VOTE
                    else TEXT['upstakes'],
            },
            'common': {
                'x': metric.get_serie(),
                'type': 'date',
                'x_format': super().DATE_FORMAT,
                'ordered_keys': ['type1', 'type2'],
            },
            'last_serie_elem': metric.get_last_serie_elem(),
            'last_value': last_value,
            'diff': metric.get_diff_last_values(add_stacks=True),
            'diff_rel': metric.get_rel_last_values(add_stacks=True),
        }
