"""
   Descp: This class is used to adapt the proposal_boost_outcome
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

class ProposalBoostOutcome(MetricAdapter):

    def __init__(self, metric_id: int) -> None:
        super().__init__(metric_id)

    
    def get_plot_data(self, o_id: str, organizations: OrganizationList) -> Dict:
        """
        Returns the metric data in a Dict using o_id param.
        """
        dao = s_factory.get_dao(
            ids=organizations.get_ids_from_id(o_id),
            metric=super().metric_id
        )
        metric: StackedSerie = dao.get_metric()

        y1 = metric.get_i_stack(0)
        y2 = metric.get_i_stack(1)
        y3 = metric.get_i_stack(2)
        y4 = metric.get_i_stack(3)

        return {
            'type1': {
                'y': y1,
                'color': Color.DARK_GREEN,
                'name': TEXT['queue_pass'],
            },
            'type2': {
                'y': y2,
                'color': Color.LIGHT_GREEN,
                'name': TEXT['boost_pass'],
            },
            'type3': {
                'y': y3,
                'color': Color.LIGHT_RED,
                'name': TEXT['boost_fail'],
            },
            'type4': {
                'y': y4,
                'color': Color.DARK_RED,
                'name': TEXT['queue_fail'],
            },
            'common': {
                'x': metric.get_serie(),
                'type': 'date',
                'x_format': MetricAdapter.DATE_FORMAT,
                'ordered_keys': ['type1', 'type2', 'type3', 'type4'],
            },
        }
