from typing import Dict
from dao_analyzer.web.apps.common.business.transfers import HierarchicalData, OrganizationList

from dao_analyzer.web.apps.common.business.i_metric_adapter import IMetricAdapter
import dao_analyzer.web.apps.aragon.data_access.daos.metric.\
    metric_dao_factory as s_factory

class AssetsValues(IMetricAdapter):
    HOVER_TEMPLATE = """%{label}<br>%{customdata[0]} $ <br>%{customdata[1]} €<br> %{customdata[2]} ETH<extra></extra>"""
    TEXT_TEMPLATE = """%{customdata[3]} %{label} <br> ~%{customdata[0]} $"""

    def get_plot_data(self, o_id: str, organizations: OrganizationList) -> Dict:
        """
        Returns the metric data in a Dict using o_id param.
        """
        dao = s_factory.get_dao(
            ids=organizations.get_ids_from_id(o_id),
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