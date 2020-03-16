"""
   Descp: A factory of dao stacked serie

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List

from src.apps.daostack.data_access.graphql.dao_stacked_serie.dao_stacked_serie \
    import DaoStackedSerie
from src.api.graphql.daostack.api_manager import ApiRequester
import src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
    st_time_serie as st_s
from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
    st_proposal_outcome import StProposalOutcome
from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
    st_total_votes import StTotalVotes


NEW_USERS = 0
NEW_PROPOSALS = 1
PROPOSALS_TYPE = 2
TOTAL_VOTES = 3


def get_dao(ids: List[str], metric: int) -> DaoStackedSerie:
    requester: ApiRequester = ApiRequester()

    stg = None
    if metric == NEW_USERS:
        stg = st_s.StTimeSerie(st_s.METRIC_TYPE_NEW_USERS)
    elif metric == NEW_PROPOSALS:
        stg = st_s.StTimeSerie(st_s.METRIC_TYPE_NEW_PROPOSAL)
    elif metric == PROPOSALS_TYPE:
        stg = StProposalOutcome()
    elif metric == TOTAL_VOTES:
        stg = StTotalVotes()

    return DaoStackedSerie(ids=ids, strategy=stg, requester=requester)
