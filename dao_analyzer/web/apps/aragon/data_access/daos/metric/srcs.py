"""
   Descp: This file stores the various sources as an enum

   Created on: 13-dec-2021

   Copyright 2021 David Davó
        <david@ddavo.me>
"""

from pathlib import Path
from typing import List

from dao_analyzer.web.apps.common.data_access.daos.metric.srcs import DATAWAREHOUSE

CACHE_PATH: Path = DATAWAREHOUSE / 'aragon'

APPS: Path = CACHE_PATH / 'apps.arr'
CASTS: Path = CACHE_PATH / 'casts.arr'
MINI_ME_TOKENS: Path = CACHE_PATH / 'miniMeTokens.arr'
ORGANIZATIONS: Path = CACHE_PATH / 'organizations.arr'
REPOS: Path = CACHE_PATH / 'repos.arr'
TOKEN_BALANCES: Path = CACHE_PATH / 'tokenBalances.arr'
TOKEN_HOLDERS: Path = CACHE_PATH / 'tokenHolders.arr'
TRANSACTIONS: Path = CACHE_PATH / 'transactions.arr'
VOTES: Path = CACHE_PATH / 'votes.arr'
ALL_FILES: List[str] = [
    APPS,
    CASTS,
    MINI_ME_TOKENS,
    ORGANIZATIONS,
    REPOS,
    TOKEN_BALANCES,
    TOKEN_HOLDERS,
    TRANSACTIONS,
    VOTES
]