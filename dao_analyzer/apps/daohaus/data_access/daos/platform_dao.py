"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 22-may-2022

   Copyright 2022-2022 David Davó Laviña
        <david@ddavo.me>
"""
import pandas as pd

from dao_analyzer.apps.common.business.transfers import Organization, OrganizationList
from dao_analyzer.apps.common.business.transfers.organization.participation_stats import MembersCreatedProposalsStat, MembersEverVotedStat
from dao_analyzer.apps.common.business.transfers.organization.platform import Platform
from dao_analyzer.apps.common.data_access.daos.platform_dao import PlatformDAO
from dao_analyzer.apps.common.data_access.requesters import CacheRequester

from .metric import srcs

class DaohausDao(PlatformDAO):
    __DF_IDX = ['network', 'molochAddress']
    __DF_DATE = 'createdAt'
    __DF_PROPOSER = 'memberAddress'
    __DF_MEMBER = 'memberAddress'
    __DF_VOTER = 'memberAddress'
    __DF_ACT_COLS = __DF_IDX + [__DF_DATE]

    __EMPTY_ADDR = '0x0000000000000000000000000000000000000000'

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

        self._membersRequester = CacheRequester([
            srcs.MEMBERS,
        ])

        self._votesRequester = CacheRequester([
            srcs.VOTES,
        ])

        self._propRequester = CacheRequester([
            srcs.PROPOSALS,
        ])
    
    def get_platform(self) -> Platform:
        df: pd.DataFrame = self._requester.request().set_index(self.__DF_IDX, drop=False)
        activity = self._activityRequester.request()
        members = self._membersRequester.request()
        participation = self._propRequester.request()
        votes = self._votesRequester.request()

        # Clean dfs
        df['summoningTime'] = pd.to_datetime(df['summoningTime'], unit='s')

        activity = activity[self.__DF_ACT_COLS]
        activity[self.__DF_DATE] = pd.to_datetime(activity[self.__DF_DATE], unit='s')

        members = members.replace(self.__EMPTY_ADDR, None)
        participation = participation.replace(self.__EMPTY_ADDR, None)

        # Getting the activity
        dfgb = activity.groupby(self.__DF_IDX)[self.__DF_DATE]
        df['first_activity'] = dfgb.min()
        df['last_activity'] = dfgb.max()

        # Getting the participation
        gbp = participation.groupby(self.__DF_IDX)
        gbm = members.groupby(self.__DF_IDX)
        gvt = votes.groupby(self.__DF_IDX)
        df['mcp_pct'] = gbp[self.__DF_PROPOSER].nunique() / gbm[self.__DF_MEMBER].nunique()
        df['mvt_pct'] = gvt[self.__DF_VOTER].nunique() / gbm[self.__DF_MEMBER].nunique()

        l: OrganizationList = OrganizationList()

        for _, org in df.iterrows():
            l.append(Organization(
                network = org['network'],
                o_id = org['molochAddress'],
                name = org['name'],
                creation_date = org['summoningTime'],
                first_activity = self._NaTtoNone(org['first_activity']),
                last_activity = self._NaTtoNone(org['last_activity']),
                participation_stats = [
                    MembersCreatedProposalsStat(org['mcp_pct']),
                    MembersEverVotedStat(org['mvt_pct']),
                ],
            ))

        mcp_pct = participation[self.__DF_PROPOSER].nunique() / members[self.__DF_MEMBER].nunique()
        mvt_pct = votes[self.__DF_VOTER].nunique() / members[self.__DF_MEMBER].nunique()
        creation_date = df['summoningTime'].min()

        return Platform(
            name = 'DAOhaus',
            creation_date=creation_date,
            organization_list = l,
            participation_stats = [
                MembersCreatedProposalsStat(mcp_pct),
                MembersEverVotedStat(mvt_pct),
            ],
        )