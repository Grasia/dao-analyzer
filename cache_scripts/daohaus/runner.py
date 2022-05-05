"""
    Descp: Daohaus Runner and Collectors

    Created on: 13-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
import requests
import requests_cache
from typing import List
from datetime import timedelta

import pandas as pd
from tqdm import tqdm
from gql.dsl import DSLField

from .. import config
from ..common.common import solve_decimals
from ..common.cryptocompare import cc_postprocessor

from ..common import ENDPOINTS, Collector
from ..common.graphql import GraphQLCollector, GraphQLRunner, add_where

DATA_ENDPOINT: str = "https://data.daohaus.club/dao/{id}"

class MembersCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('members', runner, network=network, endpoint=ENDPOINTS[network]['daohaus'])

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.members(**kwargs).select(
            ds.Member.id,
            ds.Member.createdAt,
            ds.Member.molochAddress,
            ds.Member.memberAddress,
            ds.Member.shares,
            ds.Member.loot,
            ds.Member.exists,
            ds.Member.didRagequit
        )

class MolochesCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('moloches', runner, network=network, endpoint=ENDPOINTS[network]['daohaus_stats'])

        @self.postprocessor
        def moloch_id(df: pd.DataFrame) -> pd.DataFrame:
            df['molochAddress'] = df['id']
            return df

        @self.postprocessor
        def moloch_names(df: pd.DataFrame) -> pd.DataFrame:
            df = df.rename(columns={"title":"name"})

            if config.skip_daohaus_names:
                return df

            cached = requests_cache.CachedSession(self.data_path.parent / '.names_cache', 
                use_cache_dir=False, 
                expire_after=timedelta(days=30)
            )
            tqdm.pandas(desc="Getting moloch names")
            df["name"] = df.progress_apply(lambda x:self._request_moloch_name(cached, x['id']), axis=1)

            return df
    
    @staticmethod
    def _request_moloch_name(req: requests.Session, moloch_id: str):
        response = req.get(DATA_ENDPOINT.format(id=moloch_id))

        o = response.json()
        if isinstance(o, list) and o and "name" in o[0]:
            return o[0]["name"]
        else:
            return None
    
    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.moloches(**add_where(kwargs, deleted=False)).select(
            ds.Moloch.id,
            ds.Moloch.title,
            ds.Moloch.version,
            ds.Moloch.summoner,
            ds.Moloch.summoningTime,
            ds.Moloch.timestamp,
            ds.Moloch.proposalCount,
            ds.Moloch.memberCount,
            ds.Moloch.voteCount,
            ds.Moloch.rageQuitCount,
            ds.Moloch.totalGas
        )

class ProposalsCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('proposals', runner, network=network, endpoint=ENDPOINTS[network]["daohaus"])

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.proposals(**kwargs).select(
            ds.Proposal.id,
            ds.Proposal.createdAt,
            ds.Proposal.proposalId,
            ds.Proposal.molochAddress,
            ds.Proposal.memberAddress,
            ds.Proposal.proposer,
            ds.Proposal.sponsor,
            ds.Proposal.sharesRequested,
            ds.Proposal.lootRequested,
            ds.Proposal.tributeOffered,
            ds.Proposal.paymentRequested,
            ds.Proposal.yesVotes,
            ds.Proposal.noVotes,
            ds.Proposal.sponsored,
            ds.Proposal.sponsoredAt,
            ds.Proposal.processed,
            ds.Proposal.processedAt,
            ds.Proposal.didPass,
            ds.Proposal.yesShares,
            ds.Proposal.noShares
        )
    
class RageQuitCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('rageQuits', runner, network=network, endpoint=ENDPOINTS[network]["daohaus"])

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.rageQuits(**kwargs).select(
            ds.RageQuit.id,
            ds.RageQuit.createdAt,
            ds.RageQuit.molochAddress,
            ds.RageQuit.memberAddress,
            ds.RageQuit.shares,
            ds.RageQuit.loot
        )

class TokenBalancesCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('tokenBalances', runner, network=network, endpoint=ENDPOINTS[network]["daohaus"])

        @self.postprocessor
        def change_col_names(df: pd.DataFrame) -> pd.DataFrame:
            return df.rename(columns={
                'molochId': 'molochAddress',
                'tokenTokenAddress': 'tokenAddress',
                'tokenDecimals': 'decimals',
                'tokenBalance': 'balance',
                'tokenSymbol': 'symbol'
            })

        @self.postprocessor
        def coalesce_bank_type(df: pd.DataFrame) -> pd.DataFrame:
            bank_idx = ['guildBank', 'memberBank', 'ecrowBank']

            df['bank'] = df[bank_idx].idxmax(1)
            df['bank'] = df['bank'].str.lower()
            df['bank'] = df['bank'].str.replace('bank', '')
            df = df.drop(columns=bank_idx)
        
            return df
        
        self.postprocessors.append(solve_decimals)
        self.postprocessors.append(cc_postprocessor)

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.tokenBalances(**add_where(kwargs, guildBank=True, tokenBalance_gt=0)).select(
            ds.TokenBalance.id,
            ds.TokenBalance.moloch.select(
                ds.Moloch.id
            ),
            ds.TokenBalance.token.select(
                ds.Token.tokenAddress,
                ds.Token.symbol,
                ds.Token.decimals
            ),
            ds.TokenBalance.guildBank,
            ds.TokenBalance.memberBank,
            ds.TokenBalance.ecrowBank,
            ds.TokenBalance.tokenBalance
        )

class VoteCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('votes', runner, network=network, endpoint=ENDPOINTS[network]["daohaus"])

        @self.postprocessor
        def changeColumnNames(df: pd.DataFrame) -> pd.DataFrame:
            return df.rename(columns={"proposalId":"proposalAddress"})

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.votes(**kwargs).select(
            ds.Vote.id,
            ds.Vote.createdAt,
            ds.Vote.proposal.select(ds.Proposal.id),
            ds.Vote.molochAddress,
            ds.Vote.memberAddress,
            ds.Vote.uintVote
        )

class DaohausRunner(GraphQLRunner):
    name: str = 'daohaus'

    def __init__(self):
        super().__init__()
        self._collectors: List[Collector] = []
        for n in self.networks:
            self._collectors.extend([
                MembersCollector(self, n),
                MolochesCollector(self, n),
                ProposalsCollector(self, n),
                RageQuitCollector(self, n),
                TokenBalancesCollector(self, n),
                VoteCollector(self, n)
            ])

    @property
    def collectors(self) -> List[Collector]:
        return self._collectors