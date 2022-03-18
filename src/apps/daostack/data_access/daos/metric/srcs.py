"""
   Descp: This file stores the various sources as an enum

   Created on: 13-dec-2021

   Copyright 2021 David Davó
        <david@ddavo.me>
"""

from pathlib import Path
from typing import List

CACHE_PATH: Path = Path('datawarehouse') / 'daostack'
DAOS: Path = CACHE_PATH / 'daos.arr'
PROPOSALS: Path = CACHE_PATH / 'proposals.arr'
REP_HOLDERS: Path = CACHE_PATH / 'reputationHolders.arr'
STAKES: Path = CACHE_PATH / 'stakes.arr'
TOKEN_BALANCES: Path = CACHE_PATH / 'tokenBalances.arr'
VOTES: Path = CACHE_PATH / 'votes.arr'
ALL_FILES: List[str] = [
    DAOS, 
    PROPOSALS,
    REP_HOLDERS,
    STAKES,
    TOKEN_BALANCES,
    VOTES,
]