"""
   Descp: This file stores the various sources as an enum

   Created on: 13-dec-2021

   Copyright 2021 David Davó
        <david@ddavo.me>
"""

from pathlib import Path
from typing import List
from dao_analyzer.web.apps.common.data_access.daos.metric.srcs import DATAWAREHOUSE

CACHE_PATH: Path = DATAWAREHOUSE / 'daostack'

DAOS: Path = CACHE_PATH / 'daos.arr'
PROPOSALS: Path = CACHE_PATH / 'proposals.arr'
REP_HOLDERS: Path = CACHE_PATH / 'reputationHolders.arr'
REP_MINTS: Path = CACHE_PATH / 'reputationMints.arr'
REP_BURNS: Path = CACHE_PATH / 'reputationBurns.arr'
STAKES: Path = CACHE_PATH / 'stakes.arr'
TOKEN_BALANCES: Path = CACHE_PATH / 'tokenBalances.arr'
VOTES: Path = CACHE_PATH / 'votes.arr'

ALL_FILES: List[str] = [
    DAOS, 
    PROPOSALS,
    REP_HOLDERS,
    REP_MINTS,
    REP_BURNS,
    STAKES,
    TOKEN_BALANCES,
    VOTES,
]