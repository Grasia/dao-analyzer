"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.
   Created on: 23-may-2022
   Copyright 2022-2022 David Davó Laviña
        <david@ddavo.me>
"""
import pandas as pd
import numpy as np

from dao_analyzer.web.apps.common.business.transfers import Organization, OrganizationList
from dao_analyzer.web.apps.common.business.transfers.organization.participation_stats import MembersCreatedProposalsStat, MembersEverVotedStat
from dao_analyzer.web.apps.common.business.transfers.organization.platform import Platform
from dao_analyzer.web.apps.common.data_access.daos.platform_dao import PlatformDAO
from dao_analyzer.web.apps.common.data_access.requesters import CacheRequester

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

    def _get_orgs(self) -> pd.DataFrame:
        dforgs: pd.DataFrame = self._orgsCacheRequester.request().set_index(self.__DF_IDX, drop=False)

        # Convert to datetime
        dforgs['createdAt'] = pd.to_datetime(dforgs['createdAt'], unit='s')

        return dforgs

    def _get_members(self) -> pd.DataFrame:
        dfmem: pd.DataFrame = self._membersCacheRequester.request()
        dfmem = dfmem.rename(columns={'organizationAddress': 'orgAddress'})

        members = dfmem[self.__DF_IDX + [self.__DF_MEMBER]]

        return members

    def _get_actions(self) -> pd.DataFrame:
        df = self._requester.request()
        
        # We want to concat all the actions, but they have different column names...
        actions = np.concatenate([
            df[self.__DF_IDX + [self.__DF_CAST_DATE]].dropna().to_numpy(),
            df[self.__DF_IDX + [self.__DF_VOTE_DATE]].dropna().to_numpy(),
            df[self.__DF_IDX + [self.__DF_TRANSACTION_DATE]].dropna().to_numpy(),
        ], axis=0)

        # Back to dataframe (so we can group by)
        actions = pd.DataFrame(actions, columns=self.__DF_IDX + ['actionDate'])
        actions['actionDate'] = pd.to_datetime(actions['actionDate'], unit='s')

        return actions

    def _get_creators(self, members) -> pd.DataFrame:
        creators = self._requester.request()[self.__DF_IDX + [self.__DF_PROPOSER]].dropna()

        # Creators who are also members
        creators = creators.merge(members, 
            left_on = self.__DF_IDX + [self.__DF_PROPOSER],
            right_on = self.__DF_IDX + [self.__DF_MEMBER],
        )[self.__DF_IDX + [self.__DF_PROPOSER]]

        return creators

    def _get_voters(self, members) -> pd.DataFrame:
        voters = self._requester.request()[self.__DF_IDX + [self.__DF_VOTER]].dropna()
        voters[self.__DF_VOTER] = voters[self.__DF_VOTER].str.split('-').str[2]

        # Voters who are also members
        voters = voters.merge(members,
            left_on = self.__DF_IDX + [self.__DF_VOTER],
            right_on = self.__DF_IDX + [self.__DF_MEMBER],
        )[self.__DF_IDX + [self.__DF_VOTER]]

        return voters

    def get_platform(self, orglist: OrganizationList) -> Platform:
        orgs = self._get_orgs()
        members = self._get_members()

        if orglist:
            ids = { (o.get_network(), o.get_id()) for o in orglist }

            orgs = orgs[orgs.index.isin(ids)]
            members = members[members.set_index(self.__DF_IDX).index.isin(orgs.index)]

        mcp_pct = self._get_creators(members)[self.__DF_PROPOSER].nunique() / members[self.__DF_MEMBER].nunique()
        mvp_pct = self._get_voters(members)[self.__DF_VOTER].nunique() / members[self.__DF_MEMBER].nunique()
        creation_date = orgs['createdAt'].min()

        return Platform(
            name = 'Aragon',
            creation_date = creation_date,
            networks = list(orgs['network'].unique()),
            participation_stats = [
                MembersCreatedProposalsStat(mcp_pct),
                MembersEverVotedStat(mvp_pct),
            ]
        )
    
    def get_organization_list(self) -> OrganizationList:
        dforgs = self._get_orgs()
        members = self._get_members()

        # Getting first and last activity
        dfgb = self._get_actions().groupby(self.__DF_IDX)['actionDate']

        dforgs['first_activity'] = dfgb.min()
        dforgs['last_activity'] = dfgb.max()

        # Getting the participation
        gbv = self._get_voters(members).groupby(self.__DF_IDX)
        gbp = self._get_creators(members).groupby(self.__DF_IDX)
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

        return l 
