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
from src.apps.daohaus.data_access.daos.metric.strategy.st_new_additions import StNewAdditions
from src.apps.daohaus.data_access.daos.metric.strategy.st_votes_type import StVotesType
from src.apps.daohaus.data_access.daos.metric.strategy.st_active_voters import StActiveVoters
from src.apps.daohaus.data_access.daos.metric.strategy.st_proposal_outcome import StProposalOutcome
from src.apps.daohaus.data_access.daos.metric.strategy.st_active_members import StActiveMembers 
from src.apps.daohaus.data_access.daos.metric.strategy.st_proposal_type import StProposalType
from src.apps.daohaus.data_access.daos.metric.strategy.st_active_organization import StActiveOrganization
from src.apps.daohaus.data_access.daos.metric.strategy.st_approval_proposal_rate import StApprovalProposalRate
from src.apps.daohaus.data_access.daos.metric.strategy.st_votes_voters_rate import StVoteVotersRate 

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


def get_dao(ids: List[str], metric: int) -> MetricDao:
    requester: cache.CacheRequester = None
    stg = None
    
    if metric == NEW_MEMBERS:
        stg = StNewAdditions(typ=StNewAdditions.MEMBERS)
        requester = cache.CacheRequester(srcs=[cache.MEMBERS])
    elif metric == VOTES_TYPE:
        stg = StVotesType()
        requester = cache.CacheRequester(srcs=[cache.VOTES])
    elif metric == ACTIVE_VOTERS:
        stg = StActiveVoters()
        requester = cache.CacheRequester(srcs=[cache.VOTES])
    elif metric == OUTGOING_MEMBERS:
        stg = StNewAdditions(typ=StNewAdditions.OUTGOING_MEMBERS)
        requester = cache.CacheRequester(srcs=[cache.RAGE_QUITS])
    elif metric == NEW_PROPOSALS:
        stg = StNewAdditions(typ=StNewAdditions.PROPOSALS)
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == PROPOSALS_OUTCOME:
        stg = StProposalOutcome()
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == ACTIVE_MEMBERS:
        stg = StActiveMembers()
        requester = cache.CacheRequester(srcs=[
            cache.PROPOSALS,
            cache.RAGE_QUITS,
            cache.VOTES])
    elif metric == PROPOSAL_TYPE:
        stg = StProposalType()
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == ACTIVE_ORGANIZATION:
        stg = StActiveOrganization()
        requester = cache.CacheRequester(srcs=[
            cache.PROPOSALS,
            cache.RAGE_QUITS,
            cache.VOTES])
    elif metric == APPROVAL_PROPOSAL_RATE:
        stg = StApprovalProposalRate()
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == VOTES_VOTERS_RATE:
        stg = StVoteVotersRate()
        requester = cache.CacheRequester(srcs=[cache.VOTES])

    return MetricDao(ids=ids, strategy=stg, requester=requester, address_key='molochAddress')
