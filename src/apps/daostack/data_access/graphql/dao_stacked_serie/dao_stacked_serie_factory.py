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
    st_time_serie as st_tm
from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
    st_proposal_outcome import StProposalOutcome


NEW_USERS = 0
NEW_PROPOSALS = 1
PROPOSALS_TYPE = 2


def get_dao(ids: List[str], metric: int) -> DaoStackedSerie:
    requester: ApiRequester = ApiRequester()

    st = None
    if metric == NEW_USERS:
        st = st_tm.StTimeSerie(st_tm.METRIC_TYPE_NEW_USERS)
    elif metric == NEW_PROPOSALS:
        st = st_tm.StTimeSerie(st_tm.METRIC_TYPE_NEW_PROPOSAL)
    elif metric == PROPOSALS_TYPE:
        st = StProposalOutcome()

    return DaoStackedSerie(ids=ids, strategy=st, requester=requester)
