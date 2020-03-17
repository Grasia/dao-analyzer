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
    st_proposal_boost_outcome import StProposalBoostOutcome
import src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
    st_different_voters_stakers as st_vs


NEW_USERS = 0
NEW_PROPOSALS = 1
PROPOSALS_BOOST_OUTCOME = 2
TOTAL_VOTES = 3
TOTAL_STAKES = 4
DIFFERENT_VOTERS = 5
DIFFERENT_STAKERS = 6


def get_dao(ids: List[str], metric: int) -> DaoStackedSerie:
    requester: ApiRequester = ApiRequester()

    stg = None
    if metric == NEW_USERS:
        stg = st_s.StTimeSerie(st_s.METRIC_TYPE_NEW_USERS)
    elif metric == NEW_PROPOSALS:
        stg = st_s.StTimeSerie(st_s.METRIC_TYPE_NEW_PROPOSAL)
    elif metric == TOTAL_VOTES:
        stg = st_s.StTimeSerie(st_s.METRIC_TYPE_TOTAL_VOTES)
    elif metric == TOTAL_STAKES:
        stg = st_s.StTimeSerie(st_s.METRIC_TYPE_TOTAL_STAKES)
    elif metric == PROPOSALS_BOOST_OUTCOME:
        stg = StProposalBoostOutcome()
    elif metric == DIFFERENT_VOTERS:
        stg = st_vs.StDifferentVS(st_vs.METRIC_VOTERS)
    elif metric == DIFFERENT_STAKERS:
        stg = st_vs.StDifferentVS(st_vs.METRIC_STAKERS)


    return DaoStackedSerie(ids=ids, strategy=stg, requester=requester)
