"""
   Descp: This file stores the various sources as an enum

   Created on: 13-dec-2021

   Copyright 2021 David Davó
        <david@ddavo.me>
"""

from pathlib import Path
from typing import List

from dao_analyzer.web.apps.common.data_access.daos.metric.srcs import DATAWAREHOUSE

CACHE_PATH: Path = DATAWAREHOUSE / 'daohaus'

MOLOCHES: Path = CACHE_PATH / 'moloches.arr'
PROPOSALS: Path = CACHE_PATH / 'proposals.arr'
MEMBERS: Path = CACHE_PATH / 'members.arr'
RAGE_QUITS: Path = CACHE_PATH / 'rageQuits.arr'
VOTES: Path = CACHE_PATH / 'votes.arr'
TOKEN_BALANCES: Path = CACHE_PATH / 'tokenBalances.arr'
ALL_FILES: List[str] = [MOLOCHES, PROPOSALS, MEMBERS, RAGE_QUITS, VOTES, TOKEN_BALANCES]