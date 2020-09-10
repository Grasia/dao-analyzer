"""
   Descp: Class to adapt StakedSeries in a chart. Use this class for common
          representations, in other case, you should extend this class.

   Created on: 10-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List

from src.apps.daostack.business.app_service import get_service
import src.apps.daostack.resources.colors as Color
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
import src.apps.daostack.data_access.daos.metric.\
    metric_dao_factory as s_factory

class MetricAdapter():

    DATE_FORMAT: str = '%b, %Y'

    def __init__(self, metric_id: int) -> None:
        self.__metric_id = metric_id

    
    def get_plot_data(self, o_id: str) -> Dict:
        """
        Returns the metric data in a Dict using o_id param.
        """
        dao = s_factory.get_dao(
            ids = get_service().get_organizations().get_ids_from_id(o_id),
            metric = self.__metric_id
        )
        metric: StackedSerie = dao.get_metric()

        y: List[float] = metric.get_i_stack(0)
        color = [Color.LIGHT_BLUE] * len(y)

        if color:
            color[-1] = Color.DARK_BLUE

        return {
            'x': metric.get_serie(),
            'y': y,
            'name': '',
            'color': color,
            'type': 'date',
            'x_format': MetricAdapter.DATE_FORMAT,
            'last_serie_elem': metric.get_last_serie_elem(),
            'last_value': metric.get_last_value(0),
            'diff': metric.get_diff_last_values(),
        }
