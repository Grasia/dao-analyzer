"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.
   Created on: 23-may-2022
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

class DaostackDAO(PlatformDAO):
    __DF_IDX = ['network', 'dao']

    __DF_DATE = 'createdAt'

    __DF_CLEAN_COLS = __DF_IDX + [__DF_DATE]

    __DF_PROPOSER = 'proposer'
    __DF_PROP_COLS = __DF_IDX + [__DF_PROPOSER]
    __DF_MEMBER = 'address'
    __DF_MEMBER_COLS = __DF_IDX + [__DF_MEMBER]
    __DF_VOTER = 'voter'
    __DF_VOTES_COLS = __DF_IDX + [__DF_VOTER]

    def __init__(self):
        super().__init__(CacheRequester(srcs=[
            srcs.DAOS,
        ]))

        self._activityRequester = CacheRequester(srcs=[
            srcs.PROPOSALS,
            srcs.VOTES,
            srcs.STAKES,
        ])

        self._membersRequester = CacheRequester(srcs=[
            srcs.REP_HOLDERS,
        ])

        self._votesRequester = CacheRequester(srcs=[
            srcs.VOTES,
        ])

        self._propRequester = CacheRequester(srcs=[
            srcs.PROPOSALS,
        ])

    def get_platform(self) -> Platform:
        df: pd.DataFrame = self._requester.request().set_index(self.__DF_IDX, drop=False)
        activity: pd.DataFrame = self._activityRequester.request()
        members = self._membersRequester.request()
        prop = self._propRequester.request()
        votes = self._votesRequester.request()
        
        # Clean df
        activity = activity[self.__DF_CLEAN_COLS]
        activity[self.__DF_DATE] = pd.to_datetime(activity[self.__DF_DATE], unit='s')

        members = members[self.__DF_MEMBER_COLS]
        prop = prop[self.__DF_PROP_COLS]
        votes = votes[self.__DF_VOTES_COLS]

        dfgb = activity.groupby(self.__DF_IDX)[self.__DF_DATE]
        df['first_activity'] = dfgb.min()
        df['last_activity'] = dfgb.max()

        # Only proposers that are members
        prop = prop.merge(members,
            left_on=self.__DF_IDX+[self.__DF_PROPOSER],
            right_on=self.__DF_IDX+[self.__DF_MEMBER],
        )[self.__DF_PROP_COLS]

        # Only voters that are members
        votes = votes.merge(members, 
            left_on=self.__DF_IDX+[self.__DF_VOTER],
            right_on=self.__DF_IDX+[self.__DF_MEMBER],
        )[self.__DF_VOTES_COLS]

        # Getting the participation
        gbp = prop.groupby(self.__DF_IDX)
        gbm = members.groupby(self.__DF_IDX)
        gvt = votes.groupby(self.__DF_IDX)

        df['mcp_pct'] = gbp[self.__DF_PROPOSER].nunique() / gbm[self.__DF_MEMBER].nunique()
        df['mvt_pct'] = gvt[self.__DF_VOTER].nunique() / gbm[self.__DF_MEMBER].nunique()

        l: OrganizationList = OrganizationList()

        for _, org in df.iterrows():
            l.append(Organization(
                network = org['network'],
                o_id = org['dao'],
                name = org['name'],
                creation_date = None, # We don't know how to get it
                first_activity = self._NaTtoNone(org['first_activity']),
                last_activity = self._NaTtoNone(org['last_activity']),
                participation_stats = [
                    MembersCreatedProposalsStat(org['mcp_pct']),
                    MembersEverVotedStat(org['mvt_pct']),
                ],
            ))

        mcp_pct = prop[self.__DF_PROPOSER].nunique() / members[self.__DF_MEMBER].nunique()
        mvt_pct = votes[self.__DF_VOTER].nunique() / members[self.__DF_MEMBER].nunique()
        creation_date = df['first_activity'].min()

        return Platform(
            name = 'DAOstack',
            creation_date = creation_date,
            organization_list = l,
            participation_stats = [
                MembersCreatedProposalsStat(mcp_pct),
                MembersEverVotedStat(mvt_pct),
            ]
        )
