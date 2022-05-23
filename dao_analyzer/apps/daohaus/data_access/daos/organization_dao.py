"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 22-may-2022

   Copyright 2022-2022 David Davó Laviña
        <david@ddavo.me>
"""
import pandas as pd

from dao_analyzer.apps.common.business.transfers import Organization, OrganizationList
from dao_analyzer.apps.common.data_access.daos.organization_dao import OrganizationListDao
from dao_analyzer.apps.common.data_access.requesters import CacheRequester

from .metric import srcs

class DaohausDao(OrganizationListDao):
    __DF_IDX = ['network', 'molochAddress']
    __DF_DATE = 'createdAt'
    __DF_CLEAN_COLS = __DF_IDX + [__DF_DATE]

    def __init__(self):
        super().__init__(CacheRequester(srcs=[
            srcs.MOLOCHES,
        ]))

        self._activityRequester = CacheRequester([
            srcs.MOLOCHES,
            srcs.PROPOSALS,
            srcs.RAGE_QUITS,
            srcs.VOTES,
        ])
    
    def get_organizations(self) -> OrganizationList:
        df: pd.DataFrame = self._requester.request().set_index(self.__DF_IDX, drop=False)
        activity = self._activityRequester.request()

        # Clean df
        activity = activity[self.__DF_CLEAN_COLS]
        activity[self.__DF_DATE] = pd.to_datetime(activity[self.__DF_DATE], unit='s')


        dfgb = activity.groupby(self.__DF_IDX)[self.__DF_DATE]
        df['first_activity'] = dfgb.min()
        df['last_activity'] = dfgb.max()

        l: OrganizationList = OrganizationList()

        for _, org in df.iterrows():
            l.append(Organization(
                network = org['network'],
                o_id = org['molochAddress'],
                name = org['name'],
                creation_date = pd.to_datetime(org['summoningTime'], unit='s'),
                first_activity = self._NaTtoNone(org['first_activity']),
                last_activity = self._NaTtoNone(org['last_activity']),
            ))

        return l