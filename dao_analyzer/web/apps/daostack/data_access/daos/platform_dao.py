"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.
   Created on: 23-may-2022
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

class DaostackDAO(PlatformDAO):
    __DF_IDX = ['network', 'dao']

    __DF_DATE = 'createdAt'

    __DF_CLEAN_COLS = __DF_IDX + [__DF_DATE]

    __DF_PROPOSER = 'proposer'
    __DF_PROP_COLS = __DF_IDX + [__DF_PROPOSER]
    __DF_MEMBER = 'address'
    __DF_MINT_COLS = __DF_IDX + [__DF_MEMBER, __DF_DATE]
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

        self._mintsCollector = CacheRequester(srcs=[
            srcs.REP_MINTS,
        ])

        self._votesRequester = CacheRequester(srcs=[
            srcs.VOTES,
        ])

        self._propRequester = CacheRequester(srcs=[
            srcs.PROPOSALS,
        ])

    def _get_daos(self) -> pd.DataFrame:
        return self._requester.request().set_index(self.__DF_IDX, drop=False)

    def _get_members(self) -> pd.DataFrame:
        """ Returns all members who, at one time, had some reputation """
        mints = self._mintsCollector.request()
        mints = mints[self.__DF_MINT_COLS]
        mints[self.__DF_DATE] = pd.to_datetime(mints[self.__DF_DATE], unit='s')

        return mints

    def _get_activity(self) -> pd.DataFrame:
        activity: pd.DataFrame = self._activityRequester.request()
        activity = activity[self.__DF_CLEAN_COLS]
        activity[self.__DF_DATE] = pd.to_datetime(activity[self.__DF_DATE], unit='s')
       
        return activity 

    def _get_prop(self, members: pd.DataFrame = None) -> pd.DataFrame:
        prop = self._propRequester.request()
        prop = prop[self.__DF_PROP_COLS]

        # only proposers that are members
        if members is not None:
            prop = prop.merge(members,
                left_on=self.__DF_IDX+[self.__DF_PROPOSER],
                right_on=self.__DF_IDX+[self.__DF_MEMBER],
            )[self.__DF_PROP_COLS]

        return prop

    def _get_votes(self, members: pd.DataFrame = None) -> pd.DataFrame:
        votes = self._votesRequester.request()
        
        # only voters that are members
        if members is not None:
            votes = votes.merge(members, 
                left_on=self.__DF_IDX+[self.__DF_VOTER],
                right_on=self.__DF_IDX+[self.__DF_MEMBER],
            )[self.__DF_VOTES_COLS]

        return votes

    def get_platform(self, orglist: OrganizationList = None) -> Platform:
        daos: pd.DataFrame = self._requester.request()
        
        members = self._get_members()

        if orglist:
            ids = { o.get_id() for o in orglist }

            daos = daos[daos['dao'].isin(ids)]
            members = members[members['dao'].isin(ids)]
        
        # The creation date is when the first member joined
        creation_date = members[self.__DF_DATE].min()

        mcp_pct = self._get_prop(members)[self.__DF_PROPOSER].nunique() / members[self.__DF_MEMBER].nunique()
        mvt_pct = self._get_votes(members)[self.__DF_VOTER].nunique() / members[self.__DF_MEMBER].nunique()

        return Platform(
            name = 'DAOstack',
            creation_date = creation_date,
            networks = list(daos['network'].unique()),
            participation_stats = [
                MembersCreatedProposalsStat(mcp_pct),
                MembersEverVotedStat(mvt_pct),
            ]
        )

    def get_organization_list(self) -> OrganizationList:
        df = self._get_daos()

        dfgb = self._get_activity().groupby(self.__DF_IDX)[self.__DF_DATE]
        df['first_activity'] = dfgb.min()
        df['last_activity'] = dfgb.max()

        # Getting the participation
        members = self._get_members()

        gbp = self._get_prop(members).groupby(self.__DF_IDX)
        gvt = self._get_votes(members).groupby(self.__DF_IDX)
        gbm = members.groupby(self.__DF_IDX)

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

        return l
