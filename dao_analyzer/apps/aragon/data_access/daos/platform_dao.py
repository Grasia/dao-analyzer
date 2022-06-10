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
from dao_analyzer.apps.common.business.transfers.organization.participation_stats import MembersCreatedProposalsStat, MembersEverVotedStat
from dao_analyzer.apps.common.business.transfers.organization.platform import Platform
from dao_analyzer.apps.common.data_access.daos.platform_dao import PlatformDAO
from dao_analyzer.apps.common.data_access.requesters import CacheRequester

from .metric import srcs

class AragonDAO(PlatformDAO):
    __DF_IDX = ['network', 'orgAddress']

    __DF_CAST_DATE = 'createdAt'
    __DF_VOTE_DATE = 'startDate'
    __DF_TRANSACTION_DATE = 'date'
    __DF_MEMBER = 'address'
    __DF_PROPOSER = 'originalCreator'
    __DF_VOTER = 'voter'

    def __init__(self):
        super().__init__(CacheRequester(srcs=[
            srcs.CASTS,
            srcs.VOTES,
            srcs.TRANSACTIONS,
        ]))

        self._orgsCacheRequester = CacheRequester(srcs=[srcs.ORGANIZATIONS])
        self._membersCacheRequester = CacheRequester(srcs=[srcs.TOKEN_HOLDERS])

    def get_platform(self) -> Platform:
        df: pd.DataFrame = self._requester.request()
        dforgs: pd.DataFrame = self._orgsCacheRequester.request().set_index(self.__DF_IDX, drop=False)
        dfmem: pd.DataFrame = self._membersCacheRequester.request()
        dfmem = dfmem.rename(columns={'organizationAddress': 'orgAddress'})

        # Convert to datetime
        dforgs['createdAt'] = pd.to_datetime(dforgs['createdAt'], unit='s')

        # We want to concat all the actions, but they have different column names...
        actions = np.concatenate([
            df[self.__DF_IDX + [self.__DF_CAST_DATE]].dropna().to_numpy(),
            df[self.__DF_IDX + [self.__DF_VOTE_DATE]].dropna().to_numpy(),
            df[self.__DF_IDX + [self.__DF_TRANSACTION_DATE]].dropna().to_numpy(),
        ], axis=0)
        creators = df[self.__DF_IDX + [self.__DF_PROPOSER]].dropna()
        voters = df[self.__DF_IDX + [self.__DF_VOTER]].dropna()
        voters[self.__DF_VOTER] = voters[self.__DF_VOTER].str.split('-').str[2]

        members = dfmem[self.__DF_IDX + [self.__DF_MEMBER]]

        # Creators who are also members
        creators = creators.merge(members, 
            left_on = self.__DF_IDX + [self.__DF_PROPOSER],
            right_on = self.__DF_IDX + [self.__DF_MEMBER],
        )[self.__DF_IDX + [self.__DF_PROPOSER]]

        # Voters who are also members
        voters = voters.merge(members,
            left_on = self.__DF_IDX + [self.__DF_VOTER],
            right_on = self.__DF_IDX + [self.__DF_MEMBER],
        )[self.__DF_IDX + [self.__DF_VOTER]]

        # Back to dataframe (so we can group by)
        dfActions = pd.DataFrame(actions, columns=self.__DF_IDX + ['actionDate'])
        dfActions['actionDate'] = pd.to_datetime(dfActions['actionDate'], unit='s')

        dfgb = dfActions.groupby(self.__DF_IDX)['actionDate']

        dforgs['first_activity'] = dfgb.min()
        dforgs['last_activity'] = dfgb.max()

        # Getting the participation
        gbp = creators.groupby(self.__DF_IDX)
        gbv = voters.groupby(self.__DF_IDX)
        gbm = members.groupby(self.__DF_IDX)

        dforgs['mcp_pct'] = gbp[self.__DF_PROPOSER].nunique() / gbm[self.__DF_MEMBER].nunique()
        dforgs['mcv_pct'] = gbv[self.__DF_VOTER].nunique() / gbm[self.__DF_MEMBER].nunique()

        l: OrganizationList = OrganizationList()

        for _, org in dforgs.iterrows():
            l.append(Organization(
                network = org['network'],
                o_id = org['orgAddress'],
                name = org['name'],
                creation_date = org['createdAt'],
                first_activity = self._NaTtoNone(org['first_activity']),
                last_activity = self._NaTtoNone(org['last_activity']),
                participation_stats = [
                    MembersCreatedProposalsStat(org['mcp_pct']),
                    MembersEverVotedStat(org['mcv_pct']),
                ]
            ))
        
        mcp_pct = creators[self.__DF_PROPOSER].nunique() / members[self.__DF_MEMBER].nunique()
        mvp_pct = voters[self.__DF_VOTER].nunique() / members[self.__DF_MEMBER].nunique()
        creation_date = dforgs['createdAt'].min()

        return Platform(
            name = 'Aragon',
            creation_date = creation_date,
            organization_list = l,
            participation_stats = [
                MembersCreatedProposalsStat(mcp_pct),
                MembersEverVotedStat(mvp_pct),
            ]
        )