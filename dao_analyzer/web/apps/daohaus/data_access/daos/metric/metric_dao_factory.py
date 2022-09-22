"""
   Descp: This file is used as factory to create a DAO metric

   Created on: 5-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict, Tuple
from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy

from dao_analyzer.web.apps.common.data_access.daos.metric.metric_dao \
    import MetricDao
from dao_analyzer.web.apps.common.data_access.requesters import CacheRequester, JoinCacheRequester
import dao_analyzer.web.apps.daohaus.data_access.daos.metric.srcs as srcs
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_new_additions import StNewAdditions
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_organization_activity import StOrganizationActivity
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_votes_type import StVotesType
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_active_voters import StActiveVoters
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_proposal_outcome import StProposalOutcome
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_active_members import StActiveMembers
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_proposal_type import StProposalType
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_active_organization import StActiveOrganization
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_approval_proposal_rate import StApprovalProposalRate
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_votes_voters_rate import StVoteVotersRate
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_votes_rate import StVotesRate
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_total_members import StTotalMembers
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_voters_percentage import StVotersPercentage
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_assets_values import StAssetsValues
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_assets_tokens import StAssetsTokens

NEW_MEMBERS = 0
VOTES_TYPE = 1
ACTIVE_VOTERS = 2
OUTGOING_MEMBERS = 3
NEW_PROPOSALS = 4
PROPOSALS_OUTCOME = 5
ACTIVE_MEMBERS = 6
PROPOSAL_TYPE = 7
ACTIVE_ORGANIZATION = 8
APPROVAL_PROPOSAL_RATE = 9
VOTES_VOTERS_RATE = 10
VOTES_FOR_RATE = 11
VOTES_AGAINST_RATE = 12
TOTAL_MEMBERS = 13
VOTERS_PERCENTAGE = 14
ASSETS_VALUES = 15
ASSETS_TOKENS = 16
ORGANIZATION_ACTIVITY = 17

def _metricsDefault(metric: int) -> Tuple[IMetricStrategy, CacheRequester]: # noqa: C901
    requester: CacheRequester = None
    stg = None

    if metric == NEW_MEMBERS:
        stg = StNewAdditions(typ=StNewAdditions.MEMBERS)
        requester = CacheRequester(srcs=[srcs.MEMBERS])
    elif metric == VOTES_TYPE:
        stg = StVotesType()
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == ACTIVE_VOTERS:
        stg = StActiveVoters()
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == OUTGOING_MEMBERS:
        stg = StNewAdditions(typ=StNewAdditions.OUTGOING_MEMBERS)
        requester = CacheRequester(srcs=[srcs.RAGE_QUITS])
    elif metric == NEW_PROPOSALS:
        stg = StNewAdditions(typ=StNewAdditions.PROPOSALS)
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == PROPOSALS_OUTCOME:
        stg = StProposalOutcome()
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == ACTIVE_MEMBERS:
        stg = StActiveMembers()
        requester = CacheRequester(srcs=[
            srcs.PROPOSALS,
            srcs.RAGE_QUITS,
            srcs.VOTES])
    elif metric == PROPOSAL_TYPE:
        stg = StProposalType()
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == ACTIVE_ORGANIZATION:
        stg = StActiveOrganization()
        requester = CacheRequester(srcs=[
            srcs.PROPOSALS,
            srcs.RAGE_QUITS,
            srcs.VOTES])
    elif metric == APPROVAL_PROPOSAL_RATE:
        stg = StApprovalProposalRate()
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == VOTES_VOTERS_RATE:
        stg = StVoteVotersRate()
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == VOTES_FOR_RATE:
        stg = StVotesRate(m_type=StVotesRate.VOTES_FOR)
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == VOTES_AGAINST_RATE:
        stg = StVotesRate(m_type=StVotesRate.VOTES_AGAINST)
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == TOTAL_MEMBERS:
        stg = StTotalMembers()
        requester = CacheRequester(srcs=[
            srcs.MEMBERS,
            srcs.RAGE_QUITS])
    elif metric == VOTERS_PERCENTAGE:
        stg = StVotersPercentage()
        requester = CacheRequester(srcs=[
            srcs.MEMBERS,
            srcs.RAGE_QUITS,
            srcs.VOTES])
    elif metric == ASSETS_VALUES:
        stg = StAssetsValues()
        requester = JoinCacheRequester(srcs=[
            srcs.MOLOCHES,
            srcs.TOKEN_BALANCES
        ])
    elif metric == ASSETS_TOKENS:
        stg = StAssetsTokens()
        requester = CacheRequester(srcs=[
            srcs.MOLOCHES,
            srcs.TOKEN_BALANCES
        ])
    elif metric == ORGANIZATION_ACTIVITY:
        # Same sources as ACTIVE_ORGANIZATIOn
        stg = StOrganizationActivity()
        requester = CacheRequester(srcs=[
            srcs.PROPOSALS,
            srcs.RAGE_QUITS,
            srcs.VOTES
        ])
    else:
        raise ValueError(f"Incorrect metric {metric}")

    return stg, requester

metrics_dict: Dict[int, Tuple[IMetricStrategy, CacheRequester]] = {}

def get_dao(ids: List[str], metric: int) -> MetricDao:
    if metric not in metrics_dict:
        metrics_dict[metric] = _metricsDefault(metric)

    stg, requester = metrics_dict[metric]
    return MetricDao(ids=ids, strategy=stg, requester=requester, address_key='molochAddress')
