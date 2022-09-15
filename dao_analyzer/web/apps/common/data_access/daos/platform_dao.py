"""
   Descp: This is a dao (data access object) of the platform.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 01-jun-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""
import abc
import pandas as pd

from datetime import datetime

from dao_analyzer.web.apps.common.business.transfers import Platform
from dao_analyzer.web.apps.common.business.transfers.organization.organization_list import OrganizationList
from dao_analyzer.web.apps.common.data_access.requesters.irequester import IRequester

class PlatformDAO(metaclass=abc.ABCMeta):
    def __init__(self, requester: IRequester):
        self._requester = requester

    def get_last_update_str(self) -> datetime:
        return self._requester.get_last_update_str()

    @staticmethod
    def _NaTtoNone(d) -> datetime:
        return None if pd.isna(d) else d

    @abc.abstractmethod
    def get_platform(self, orglist: OrganizationList = None) -> Platform:
        """Gets the platform

        Args:
            orglist (OrganizationList, optional): If not None, limits the organizations used to get the platform info. Defaults to None.

        Returns:
            Platform: The object with the platform information
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_organization_list(self) -> OrganizationList:
        """Gets the organization list

        Returns:
            OrganizationList: The organization list with all its attributes
        """
        raise NotImplementedError
