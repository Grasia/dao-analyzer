"""
   Descp: This class is used to adapt the PROPOSALS_BOOST_SUCCES_RATIO
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
from dao_analyzer.web.apps.common.business.transfers.n_stacked_serie import NStackedSerie
import dao_analyzer.web.apps.daostack.data_access.daos.metric.\
    metric_dao_factory as s_factory

class SuccessRatioType(MetricAdapter):

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
        metric: NStackedSerie = dao.get_metric()

        y1 = metric.get_i_sserie(0).get_i_stack(0)
        y2 = metric.get_i_sserie(1).get_i_stack(0)

        return {
            'type1': {
                'y': y1,
                'color': Color.LIGHT_GREEN,
                'name': TEXT['boost'],
            },
            'type2': {
                'y': y2,
                'color': Color.DARK_RED,
                'name': TEXT['not_boost'],
            },
            'common': {
                'x': metric.get_serie(),
                'type': 'date',
                'x_format': super().DATE_FORMAT,
                'ordered_keys': ['type1', 'type2'],
            }
        }
