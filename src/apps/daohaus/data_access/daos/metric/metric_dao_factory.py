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
import src.apps.daohaus.data_access.daos.metric.strategy.st_new_members as mem


NEW_MEMBERS = 0


def get_dao(ids: List[str], metric: int) -> MetricDao:
    requester: cache.CacheRequester = None
    stg = None
    
    if metric == NEW_MEMBERS:
        stg = mem.StNewMembers()
        requester = cache.CacheRequester(srcs=[cache.MEMBERS])

    return MetricDao(ids=ids, strategy=stg, requester=requester)
