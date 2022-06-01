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

from dao_analyzer.apps.common.business.transfers import Platform
from dao_analyzer.apps.common.data_access.requesters.irequester import IRequester

class PlatformDAO(metaclass=abc.ABCMeta):
    def __init__(self, requester: IRequester):
        self._requester = requester

    def get_last_update_str(self) -> datetime:
        return self._requester.get_last_update_str()

    @staticmethod
    def _NaTtoNone(d) -> datetime:
        return None if pd.isna(d) else d

    @abc.abstractmethod
    def get_platform(self) -> Platform:
        raise NotImplementedError
