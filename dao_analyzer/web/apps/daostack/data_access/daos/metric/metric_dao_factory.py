"""
   Descp: A factory of dao stacked serie

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict, Tuple
from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy

from dao_analyzer.web.apps.common.data_access.daos.metric.metric_dao \
    import MetricDao
from dao_analyzer.web.apps.common.data_access.requesters import CacheRequester, JoinCacheRequester
import dao_analyzer.web.apps.daostack.data_access.daos.metric.srcs as srcs
import dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_time_serie as st_s
import dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_proposal_outcome as st_po
import dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_different_voters_stakers as st_vs
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_proposal_majority import StProposalMajority
import dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_total_votes_stakes_option as st_tvso
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_active_users\
    import StActiveUsers
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_active_organization\
    import StActiveOrganization
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_approval_proposal_rate\
    import StApprovalProposalRate
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_assets_tokens import StAssetsTokens
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_assets_values import StAssetsValues
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_votes_voters_rate\
    import StVoteVotersRate
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_votes_rate\
    import StVotesRate
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_total_reputation_holders\
    import StTotalRepHolders
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_voters_percentage\
    import StVotersPercentage
from .strategy.st_organization_activity import StOrganizationActivity

NEW_USERS = 0
NEW_PROPOSALS = 1
PROPOSALS_BOOST_OUTCOME = 2
TOTAL_VOTES = 3
TOTAL_STAKES = 4
DIFFERENT_VOTERS = 5
DIFFERENT_STAKERS = 6
PROPOSAL_MAJORITY = 7
PROPOSALS_TOTAL_SUCCES_RATIO = 8
PROPOSALS_BOOST_SUCCES_RATIO = 9
TOTAL_VOTES_OPTION = 10
TOTAL_STAKES_OPTION = 11
ACTIVE_USERS = 12
ACTIVE_ORGANIZATION = 13
APPROVAL_PROPOSAL_RATE = 14
VOTE_VOTERS_RATE = 15
VOTES_FOR_RATE = 16
VOTES_AGAINST_RATE = 17
TOTAL_REP_HOLDERS = 18
VOTERS_PERCENTAGE = 19
ASSETS_VALUES = 20
ASSETS_TOKENS = 21
ORGANIZATION_ACTIVITY = 22

# TODO: Do this in the other files or MISS
def _metricsDefault(metric: int) -> Tuple[IMetricStrategy, CacheRequester]: # noqa: C901
    requester: CacheRequester = None
    stg = None

    if metric == NEW_USERS:
        stg = st_s.StTimeSerie(st_s.NEW_USERS)
        requester = CacheRequester(srcs=[srcs.REP_HOLDERS])
    elif metric == NEW_PROPOSALS:
        stg = st_s.StTimeSerie(st_s.NEW_PROPOSAL)
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == TOTAL_VOTES:
        stg = st_s.StTimeSerie(st_s.TOTAL_VOTES)
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == TOTAL_STAKES:
        stg = st_s.StTimeSerie(st_s.TOTAL_STAKES)
        requester = CacheRequester(srcs=[srcs.STAKES])
    elif metric == PROPOSALS_BOOST_OUTCOME:
        stg = st_po.StProposalOutcome(st_po.BOOST_OUTCOME)
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == DIFFERENT_VOTERS:
        stg = st_vs.StDifferentVS(st_vs.VOTERS)
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == DIFFERENT_STAKERS:
        stg = st_vs.StDifferentVS(st_vs.STAKERS)
        requester = CacheRequester(srcs=[srcs.STAKES])
    elif metric == PROPOSAL_MAJORITY:
        stg = StProposalMajority()
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == PROPOSALS_TOTAL_SUCCES_RATIO:
        stg = st_po.StProposalOutcome(st_po.TOTAL_SUCCESS_RATIO)
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == PROPOSALS_BOOST_SUCCES_RATIO:
        stg = st_po.StProposalOutcome(st_po.BOOST_SUCCESS_RATIO)
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == TOTAL_VOTES_OPTION:
        stg = st_tvso.StTotalVSOption(st_tvso.VOTES)
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == TOTAL_STAKES_OPTION:
        stg = st_tvso.StTotalVSOption(st_tvso.STAKES)
        requester = CacheRequester(srcs=[srcs.STAKES])
    elif metric == ACTIVE_USERS:
        stg = StActiveUsers()
        requester = CacheRequester(srcs=[
            srcs.PROPOSALS, 
            srcs.VOTES, 
            srcs.STAKES])
    elif metric == ACTIVE_ORGANIZATION:
        stg = StActiveOrganization()
        requester = CacheRequester(srcs=[
            srcs.PROPOSALS,
            srcs.VOTES,
            srcs.STAKES])
    elif metric == APPROVAL_PROPOSAL_RATE:
        stg = StApprovalProposalRate()
        requester = CacheRequester(srcs=[srcs.PROPOSALS])
    elif metric == VOTE_VOTERS_RATE:
        stg = StVoteVotersRate()
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == VOTES_FOR_RATE:
        stg = StVotesRate(m_type=StVotesRate.VOTES_FOR)
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == VOTES_AGAINST_RATE:
        stg = StVotesRate(m_type=StVotesRate.VOTES_AGAINST)
        requester = CacheRequester(srcs=[srcs.VOTES])
    elif metric == TOTAL_REP_HOLDERS:
        stg = StTotalRepHolders()
        requester = CacheRequester(srcs=[srcs.REP_HOLDERS])
    elif metric == VOTERS_PERCENTAGE:
        stg = StVotersPercentage()
        requester = CacheRequester(srcs=[
            srcs.REP_HOLDERS,
            srcs.VOTES])
    elif metric == ASSETS_TOKENS:
        stg = StAssetsTokens()
        requester = JoinCacheRequester(srcs=[
            srcs.DAOS,
            srcs.TOKEN_BALANCES
        ])
    elif metric == ASSETS_VALUES:
        stg = StAssetsValues()
        requester = JoinCacheRequester(srcs=[
            srcs.DAOS,
            srcs.TOKEN_BALANCES
        ])
    elif metric == ORGANIZATION_ACTIVITY:
        stg = StOrganizationActivity()
        requester = CacheRequester(srcs=[
            srcs.PROPOSALS,
            srcs.VOTES,
            srcs.STAKES])
    else:
        raise ValueError(f"Incorrect metric: {metric}")
    
    return stg, requester

metrics_dict: Dict[int, Tuple[IMetricStrategy, CacheRequester]] = {}

def get_dao(ids: List[str], metric: int) -> MetricDao:
    if metric not in metrics_dict:
        metrics_dict[metric] = _metricsDefault(metric)

    stg, requester = metrics_dict[metric]
    return MetricDao(ids=ids, strategy=stg, requester=requester, address_key='dao')
