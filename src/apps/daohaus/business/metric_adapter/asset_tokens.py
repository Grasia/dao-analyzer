from typing import Callable, Dict

import pandas as pd

# from src.apps.common.business.transfers.tabular_data import TabularData
from src.apps.common.business.transfers.organization import OrganizationList
from src.apps.common.business.i_metric_adapter import IMetricAdapter
import src.apps.daohaus.data_access.daos.metric.metric_dao_factory as s_factory

class AssetsTokens(IMetricAdapter):
    def __init__(self, organizations: Callable[...,OrganizationList]) -> None:
        self.__organizations = organizations

    @property
    def organizations(self) -> OrganizationList:
        return self.__organizations()

    def get_plot_data(self, o_id: str) -> Dict:
        """
        Returns the metric data in a Dict using o_id param
        """
        dao = s_factory.get_dao(
            ids=self.organizations.get_ids_from_id(o_id),
            metric=s_factory.ASSETS_TOKENS
        )

        return dao.get_metric()