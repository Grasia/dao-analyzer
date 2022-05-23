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
from dao_analyzer.apps.common.data_access.requesters import JoinCacheRequester

from .metric import srcs

class DaohausDao(OrganizationListDao):
    __DF_IDX = ['network', 'molochAddress']
    __DF_GB_COLS = __DF_IDX + ['name', 'summoningTime']
    __DF_USED_COLS = __DF_GB_COLS + ['createdAt']

    def __init__(self):
        super().__init__(JoinCacheRequester(srcs=[
            srcs.MOLOCHES,
            srcs.PROPOSALS,
            srcs.RAGE_QUITS,
            srcs.VOTES,
        ], how='left', on=self.__DF_IDX))
    
    def get_organizations(self) -> OrganizationList:
        df: pd.DataFrame = self._requester.request()

        df['createdAt'] = pd.to_datetime(df['createdAt'], unit='s')

        # Cleaning the df
        df = df[self.__DF_USED_COLS]

        dfgb = df.groupby(self.__DF_GB_COLS)

        l: OrganizationList = OrganizationList()


        for idx, g in dfgb:
            l.append(Organization(
                network = idx[0],
                o_id = idx[1],
                name = idx[2],
                creation_date = pd.to_datetime(idx[3], unit='s'),
                first_activity = self._NaTtoNone(g['createdAt'].min()),
                last_activity = self._NaTtoNone(g['createdAt'].max()),
            ))

        return l