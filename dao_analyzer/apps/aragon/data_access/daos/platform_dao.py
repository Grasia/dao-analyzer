"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.
   Created on: 23-may-2022
   Copyright 2022-2022 David Davó Laviña
        <david@ddavo.me>
"""
import pandas as pd
import numpy as np

from dao_analyzer.apps.common.business.transfers import Organization, OrganizationList
from dao_analyzer.apps.common.business.transfers.organization.platform import Platform
from dao_analyzer.apps.common.data_access.daos.platform_dao import PlatformDAO
from dao_analyzer.apps.common.data_access.requesters import CacheRequester

from .metric import srcs

class AragonDAO(PlatformDAO):
    __DF_IDX = ['network', 'orgAddress']

    __DF_CAST_DATE = 'createdAt'
    __DF_VOTE_DATE = 'startDate'
    __DF_TRANSACTION_DATE = 'date'

    def __init__(self):
        super().__init__(CacheRequester(srcs=[
            srcs.CASTS,
            srcs.VOTES,
            srcs.TRANSACTIONS,
        ]))

        self._orgsCacheRequester = CacheRequester(srcs=[srcs.ORGANIZATIONS])

    def get_platform(self) -> Platform:
        df: pd.DataFrame = self._requester.request()
        dforgs: pd.DataFrame = self._orgsCacheRequester.request().set_index(self.__DF_IDX, drop=False)

        # Convert to datetime
        dforgs['createdAt'] = pd.to_datetime(dforgs['createdAt'], unit='s')

        # We want to concat all the actions, but they have different column names...
        actions = np.concatenate([
            df[self.__DF_IDX + [self.__DF_CAST_DATE]].dropna().to_numpy(),
            df[self.__DF_IDX + [self.__DF_VOTE_DATE]].dropna().to_numpy(),
            df[self.__DF_IDX + [self.__DF_TRANSACTION_DATE]].dropna().to_numpy(),
        ], axis=0)

        # Back to dataframe (so we can group by)
        dfActions = pd.DataFrame(actions, columns=self.__DF_IDX + ['actionDate'])
        dfActions['actionDate'] = pd.to_datetime(dfActions['actionDate'], unit='s')

        dfgb = dfActions.groupby(self.__DF_IDX)['actionDate']

        dforgs['first_activity'] = dfgb.min()
        dforgs['last_activity'] = dfgb.max()

        l: OrganizationList = OrganizationList()

        for _, org in dforgs.iterrows():
            l.append(Organization(
                network = org['network'],
                o_id = org['orgAddress'],
                name = org['name'],
                creation_date = org['createdAt'],
                first_activity = self._NaTtoNone(org['first_activity']),
                last_activity = self._NaTtoNone(org['last_activity']),
            ))
        
        creation_date = dforgs['createdAt'].min()

        return Platform(
            name = 'Aragon',
            creation_date = creation_date,
            organization_list = l,
        )