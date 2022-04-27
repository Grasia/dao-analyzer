from typing import Callable, Dict
from dao_analyzer.apps.common.business.transfers import HierarchicalData, OrganizationList

from dao_analyzer.apps.common.business.i_metric_adapter import IMetricAdapter
import dao_analyzer.apps.daostack.data_access.daos.metric.\
    metric_dao_factory as s_factory

class AssetsValues(IMetricAdapter):
    HOVER_TEMPLATE = """%{label}<br>%{customdata[0]} $ <br>%{customdata[1]} €<br> %{customdata[2]} ETH<extra></extra>"""
    TEXT_TEMPLATE = """%{customdata[3]} %{label} <br> ~%{customdata[0]} $"""

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
            metric=s_factory.ASSETS_VALUES
        )

        metric: HierarchicalData = dao.get_metric()

        return {
            **metric.to_dict(),
            'root_color': 'lightgrey',
            'hovertemplate': self.HOVER_TEMPLATE,
            'texttemplate': self.TEXT_TEMPLATE,
            'branchvalues': 'remainder'
        } 