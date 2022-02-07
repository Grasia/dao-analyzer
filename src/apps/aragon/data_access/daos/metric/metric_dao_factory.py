"""
   Descp: This file is used as factory to create a DAO metric

   Created on: 19-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict, Tuple
from src.apps.common.data_access.daos.metric.imetric_strategy import IMetricStrategy

from src.apps.common.data_access.daos.metric.metric_dao \
    import MetricDao
from src.apps.common.data_access.requesters.cache_requester import CacheRequester
import src.apps.aragon.data_access.daos.metric.srcs as srcs
from src.apps.aragon.data_access.daos.metric.strategy.st_new_additions import StNewAdditions
from src.apps.aragon.data_access.daos.metric.strategy.st_installed_apps import StInstalledApps
from src.apps.aragon.data_access.daos.metric.strategy.st_cast_type import StCastType
from src.apps.aragon.data_access.daos.metric.strategy.st_vote_outcome import StVoteOutcome
from src.apps.aragon.data_access.daos.metric.strategy.st_active_voters import StActiveVoters
from src.apps.aragon.data_access.daos.metric.strategy.st_active_token_holders import StActiveTokenHolders
from src.apps.aragon.data_access.daos.metric.strategy.st_active_organization import StActiveOrganization
from src.apps.aragon.data_access.daos.metric.strategy.st_approval_vote_rate import StApprovalVoteRate
from src.apps.aragon.data_access.daos.metric.strategy.st_casted_votes_voters_rate import StVoteVotersRate
from src.apps.aragon.data_access.daos.metric.strategy.st_casted_votes_rate import StCastedVotesRate


NEW_VOTES = 0
NEW_TRANSACTIONS = 1
INSTALLED_APPS = 2
CAST_TYPE = 3
VOTE_OUTCOME = 4
ACTIVE_VOTERS = 5
ACTIVE_TOKEN_HOLDERS = 6
ACTIVE_ORGANIZATION = 7
APPROVAL_VOTE_RATE = 8
CASTED_VOTE_VOTER_RATE = 9
CASTED_VOTE_FOR_RATE = 10
CASTED_VOTE_AGAINST_RATE = 11


def _metricsDefault(metric: int) -> Tuple[IMetricStrategy, CacheRequester]: # noqa: C901
    address_key: str = ''
    requester: CacheRequester = None
    stg = None

    if metric == NEW_VOTES:
        stg = StNewAdditions(typ=StNewAdditions.VOTE)
        requester = CacheRequester(srcs=[srcs.VOTES])
        address_key = 'orgAddress'
    elif metric == NEW_TRANSACTIONS:
        stg = StNewAdditions(typ=StNewAdditions.TRANSACTION)
        requester = CacheRequester(srcs=[srcs.TRANSACTIONS])
        address_key = 'orgAddress'
    elif metric == INSTALLED_APPS:
        stg = StInstalledApps()
        requester = CacheRequester(srcs=[srcs.APPS])
        address_key = 'organizationId'
    elif metric == CAST_TYPE:
        stg = StCastType()
        requester = CacheRequester(srcs=[srcs.CASTS])
        address_key = 'orgAddress'
    elif metric == VOTE_OUTCOME:
        stg = StVoteOutcome()
        requester = CacheRequester(srcs=[srcs.VOTES])
        address_key = 'orgAddress'
    elif metric == ACTIVE_VOTERS:
        stg = StActiveVoters()
        requester = CacheRequester(srcs=[srcs.CASTS])
        address_key = 'orgAddress'
    elif metric == ACTIVE_TOKEN_HOLDERS:
        stg = StActiveTokenHolders()
        requester = CacheRequester(srcs=[
            srcs.CASTS,
            srcs.VOTES,
            srcs.TRANSACTIONS])
        address_key = 'orgAddress'
    elif metric == ACTIVE_ORGANIZATION:
        stg = StActiveOrganization()
        requester = CacheRequester(srcs=[
            srcs.CASTS,
            srcs.VOTES,
            srcs.TRANSACTIONS])
        address_key = 'orgAddress'
    elif metric == APPROVAL_VOTE_RATE:
        stg = StApprovalVoteRate()
        requester = CacheRequester(srcs=[srcs.VOTES])
        address_key = 'orgAddress'
    elif metric == CASTED_VOTE_VOTER_RATE:
        stg = StVoteVotersRate()
        requester = CacheRequester(srcs=[srcs.CASTS])
        address_key = 'orgAddress'
    elif metric == CASTED_VOTE_FOR_RATE:
        stg = StCastedVotesRate(m_type=StCastedVotesRate.CAST_VOTE_FOR)
        requester = CacheRequester(srcs=[srcs.CASTS])
        address_key = 'orgAddress'
    elif metric == CASTED_VOTE_AGAINST_RATE:
        stg = StCastedVotesRate(m_type=StCastedVotesRate.CAST_VOTE_AGAINST)
        requester = CacheRequester(srcs=[srcs.CASTS])
        address_key = 'orgAddress'

    return stg, requester, address_key

metrics_dict: Dict[int, Tuple[IMetricStrategy, CacheRequester, str]] = {}

def get_dao(ids: List[str], metric: int) -> MetricDao:
    if metric not in metrics_dict:
        metrics_dict[metric] = _metricsDefault(metric)

    stg, requester, address_key = metrics_dict[metric]
    return MetricDao(ids=ids, strategy=stg, requester=requester, address_key=address_key)
