"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 22-may-2022

   Copyright 2022-2022 David Davó Laviña
        <david@ddavo.me>
"""
import pandas as pd

from dao_analyzer.web.apps.common.business.transfers import Organization, OrganizationList
from dao_analyzer.web.apps.common.business.transfers.organization.participation_stats import MembersCreatedProposalsStat, MembersEverVotedStat
from dao_analyzer.web.apps.common.business.transfers.organization.platform import Platform
from dao_analyzer.web.apps.common.data_access.daos.platform_dao import PlatformDAO
from dao_analyzer.web.apps.common.data_access.requesters import CacheRequester

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

    def _get_daos(self) -> pd.DataFrame:
        df = self._requester.request().set_index(self.__DF_IDX, drop=False)

        df['summoningTime'] = pd.to_datetime(df['summoningTime'], unit='s')

        return df

    @staticmethod
    def _filter_by_daos(df, daos) -> pd.DataFrame:
        if daos is None:
            return df
        else:
            return df[df.set_index(DaohausDao.__DF_IDX).index.isin(daos.index)]

    def _get_participation(self, daos: pd.DataFrame = None) -> pd.DataFrame:
        participation = self._propRequester.request()
        participation = participation.replace(self.__EMPTY_ADDR, None)

        participation = self._filter_by_daos(participation, daos)

        return participation

    def _get_activity(self) -> pd.DataFrame:
        activity = self._activityRequester.request()
        activity = activity[self.__DF_ACT_COLS]
        activity[self.__DF_DATE] = pd.to_datetime(activity[self.__DF_DATE], unit='s')

        return activity

    def _get_members(self) -> pd.DataFrame:
        members = self._membersRequester.request()
        members = members.replace(self.__EMPTY_ADDR, None)

        return members

    def _get_votes(self, daos: pd.DataFrame = None) -> pd.DataFrame:
        votes = self._votesRequester.request()

        votes = self._filter_by_daos(votes, daos)

        return votes

    def get_platform(self, orglist: OrganizationList) -> Platform:
        df = self._get_daos()
        members = self._get_members()

        if orglist:
            ids = { (o.get_network(), o.get_id()) for o in orglist }
            
            df = df[df.index.isin(ids)]
            members = self._filter_by_daos(members, df)

        mcp_pct = self._get_participation(daos=df)[self.__DF_PROPOSER].nunique() / members[self.__DF_MEMBER].nunique()
        mvt_pct = self._get_votes(daos=df)[self.__DF_VOTER].nunique() / members[self.__DF_MEMBER].nunique()
        creation_date = df['summoningTime'].min()

        return Platform(
            name = 'DAOhaus',
            creation_date=creation_date,
            networks=list(df['network'].unique()),
            participation_stats = [
                MembersCreatedProposalsStat(mcp_pct),
                MembersEverVotedStat(mvt_pct),
            ],
        )

    def get_organization_list(self) -> OrganizationList:
        df = self._get_daos()
        members = self._get_members()

        # Getting the participation
        gbp = self._get_participation().groupby(self.__DF_IDX)
        gvt = self._get_votes().groupby(self.__DF_IDX)
        gbm = members.groupby(self.__DF_IDX)
        df['mcp_pct'] = gbp[self.__DF_PROPOSER].nunique() / gbm[self.__DF_MEMBER].nunique()
        df['mvt_pct'] = gvt[self.__DF_VOTER].nunique() / gbm[self.__DF_MEMBER].nunique()

        # Getting the activity
        dfgb = self._get_activity().groupby(self.__DF_IDX)[self.__DF_DATE]
        df['first_activity'] = dfgb.min()
        df['last_activity'] = dfgb.max()

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

        return l
