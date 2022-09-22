"""
   Descp: This class is used to adapt the proposal majority
          metric to its visual representation.

   Created on: 14-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List
from dao_analyzer.web.apps.common.business.transfers.organization.organization_list import OrganizationList

import dao_analyzer.web.apps.common.resources.colors as Color
from dao_analyzer.web.apps.daostack.resources.strings import TEXT
from dao_analyzer.web.apps.daostack.business.metric_adapter.metric_adapter import MetricAdapter
from dao_analyzer.web.apps.common.business.transfers.n_stacked_serie import NStackedSerie
import dao_analyzer.web.apps.daostack.data_access.daos.metric.\
    metric_dao_factory as s_factory

class MajorityType(MetricAdapter):
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

        y1 = metric.get_i_sserie(0)
        y2 = metric.get_i_sserie(1)
        y3 = metric.get_i_sserie(2)
        y4 = metric.get_i_sserie(3)
        x: List = y1.get_serie()

        return {
            'type1': {
                'x': y1.get_serie(),
                'y': y1.get_i_stack(0),
                'color': f'rgba{Color.hex_to_rgba(Color.DARK_GREEN, 0.5)}',
                'marker_symbol': 'triangle-up',
                'name': TEXT['abs_pass'],
                'position': 'up',
            },
            'type2': {
                'x': y2.get_serie(),
                'y': y2.get_i_stack(0),
                'color': f'rgba{Color.hex_to_rgba(Color.DARK_GREEN, 0.5)}',
                'marker_symbol': 'circle',
                'name': TEXT['rel_pass'],
                'position': 'up',
            },
            'type3': {
                'x': y3.get_serie(),
                'y': y3.get_i_stack(0),
                'color': f'rgba{Color.hex_to_rgba(Color.DARK_RED, 0.5)}',
                'marker_symbol': 'circle',
                'name': TEXT['rel_fail'],
                'position': 'down',
            },
            'type4': {
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
                'x_format': super().DATE_FORMAT,
                'ordered_keys': ['type1', 'type2', 'type3', 'type4'], 
                'y_suffix': '%',
            }
        }
