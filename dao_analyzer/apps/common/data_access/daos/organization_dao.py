"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 17-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
import abc
import pandas as pd

from datetime import datetime

from dao_analyzer.apps.common.business.transfers.organization import OrganizationList
from dao_analyzer.apps.common.data_access.requesters.irequester import IRequester


class OrganizationListDao(metaclass=abc.ABCMeta):
    def __init__(self, requester: IRequester):
        self._requester = requester

    def get_last_update_str(self) -> datetime:
        return self._requester.get_last_update_str()

    @staticmethod
    def _NaTtoNone(d) -> datetime:
        return None if pd.isnull(d) else d

    @abc.abstractmethod
    def get_organizations(self) -> OrganizationList:
        raise NotImplementedError
