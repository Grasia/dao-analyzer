"""
   Descp: This file is used as factory to create a DAO metric

   Created on: 5-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import List

from src.apps.common.data_access.daos.metric.metric_dao \
    import MetricDao
import src.apps.daohaus.data_access.requesters.cache_requester as cache
from src.apps.daohaus.data_access.daos.metric.strategy.st_new_members import StNewMembers
from src.apps.daohaus.data_access.daos.metric.strategy.st_votes_type import StVotesType
from src.apps.daohaus.data_access.daos.metric.strategy.st_active_voters import StActiveVoters

NEW_MEMBERS = 0
VOTES_TYPE = 1
ACTIVE_VOTERS = 2


def get_dao(ids: List[str], metric: int) -> MetricDao:
    requester: cache.CacheRequester = None
    stg = None
    
    if metric == NEW_MEMBERS:
        stg = StNewMembers()
        requester = cache.CacheRequester(srcs=[cache.MEMBERS])
    elif metric == VOTES_TYPE:
        stg = StVotesType()
        requester = cache.CacheRequester(srcs=[cache.VOTES])
    elif metric == ACTIVE_VOTERS:
        stg = StActiveVoters()
        requester = cache.CacheRequester(srcs=[cache.VOTES])

    return MetricDao(ids=ids, strategy=stg, requester=requester, address_key='molochAddress')
