"""
   Descp: This file is used as factory to create a DAO metric

   Created on: 19-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import List

from src.apps.common.data_access.daos.metric.metric_dao \
    import MetricDao
import src.apps.aragon.data_access.requesters.cache_requester as cache
from src.apps.aragon.data_access.daos.metric.strategy.st_new_additions import StNewAdditions
from src.apps.aragon.data_access.daos.metric.strategy.st_installed_apps import StInstalledApps
from src.apps.aragon.data_access.daos.metric.strategy.st_cast_type import StCastType
from src.apps.aragon.data_access.daos.metric.strategy.st_vote_outcome import StVoteOutcome
from src.apps.aragon.data_access.daos.metric.strategy.st_active_voters import StActiveVoters
from src.apps.aragon.data_access.daos.metric.strategy.st_active_token_holders import StActiveTokenHolders
from src.apps.aragon.data_access.daos.metric.strategy.st_active_organization import StActiveOrganization
from src.apps.aragon.data_access.daos.metric.strategy.st_approval_vote_rate import StApprovalVoteRate


NEW_VOTES = 0
NEW_TRANSACTIONS = 1
INSTALLED_APPS = 2
CAST_TYPE = 3
VOTE_OUTCOME = 4
ACTIVE_VOTERS = 5
ACTIVE_TOKEN_HOLDERS = 6
ACTIVE_ORGANIZATION = 7
APPROVAL_VOTE_RATE = 8


def get_dao(ids: List[str], metric: int) -> MetricDao:
    address_key: str = ''
    requester: cache.CacheRequester = None
    stg = None
    
    if metric == NEW_VOTES:
        stg = StNewAdditions(typ=StNewAdditions.VOTE)
        requester = cache.CacheRequester(srcs=[cache.VOTES])
        address_key = 'orgAddress'
    elif metric == NEW_TRANSACTIONS:
        stg = StNewAdditions(typ=StNewAdditions.TRANSACTION)
        requester = cache.CacheRequester(srcs=[cache.TRANSACTIONS])
        address_key = 'orgAddress'
    elif metric == INSTALLED_APPS:
        stg = StInstalledApps()
        requester = cache.CacheRequester(srcs=[cache.APPS])
        address_key = 'organizationId'
    elif metric == CAST_TYPE:
        stg = StCastType()
        requester = cache.CacheRequester(srcs=[cache.CASTS])
        address_key = 'orgAddress'
    elif metric == VOTE_OUTCOME:
        stg = StVoteOutcome()
        requester = cache.CacheRequester(srcs=[cache.VOTES])
        address_key = 'orgAddress'
    elif metric == ACTIVE_VOTERS:
        stg = StActiveVoters()
        requester = cache.CacheRequester(srcs=[cache.CASTS])
        address_key = 'orgAddress'
    elif metric == ACTIVE_TOKEN_HOLDERS:
        stg = StActiveTokenHolders()
        requester = cache.CacheRequester(srcs=[
            cache.CASTS,
            cache.VOTES,
            cache.TRANSACTIONS])
        address_key = 'orgAddress'
    elif metric == ACTIVE_ORGANIZATION:
        stg = StActiveOrganization()
        requester = cache.CacheRequester(srcs=[
            cache.CASTS,
            cache.VOTES,
            cache.TRANSACTIONS])
        address_key = 'orgAddress'
    elif metric == APPROVAL_VOTE_RATE:
        stg = StApprovalVoteRate()
        requester = cache.CacheRequester(srcs=[cache.VOTES])
        address_key = 'orgAddress'

    return MetricDao(ids=ids, strategy=stg, requester=requester, address_key=address_key)
