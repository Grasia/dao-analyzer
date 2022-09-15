from typing import Dict

from dao_analyzer.web.apps.common.business.transfers import TabularData, OrganizationList
from dao_analyzer.web.apps.common.business.i_metric_adapter import IMetricAdapter
import dao_analyzer.web.apps.daohaus.data_access.daos.metric.metric_dao_factory as s_factory

class AssetsTokens(IMetricAdapter):
    def get_plot_data(self, o_id: str, organizations: OrganizationList) -> Dict:
        """
        Returns the metric data in a Dict using o_id param
        """
        dao: TabularData = s_factory.get_dao(
            ids=organizations.get_ids_from_id(o_id),
            metric=s_factory.ASSETS_TOKENS
        )

        return dao.get_metric()