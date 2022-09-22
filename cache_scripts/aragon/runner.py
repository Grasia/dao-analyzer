"""
    Descp: Aragon Runner and Collectors

    Created on: 02-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from typing import List

import pkgutil
from gql.dsl import DSLField
import pandas as pd
import numpy as np
import json

from ..aragon import __name__ as aragon_module_name
from ..common.cryptocompare import CCPricesCollector
from ..common import ENDPOINTS, Collector
from ..common.graphql import GraphQLCollector, GraphQLRunner
from ..common.blockscout import BlockscoutBallancesCollector

class AppsCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('apps', runner, endpoint=ENDPOINTS[network]['aragon'], network=network)

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.apps(**kwargs).select(
            ds.App.id,
            ds.App.isForwarder,
            ds.App.isUpgradeable,
            ds.App.repoName,
            ds.App.repoAddress,
            ds.App.organization.select(ds.Organization.id)
        )

class BalancesCollector(BlockscoutBallancesCollector):
    def __init__(self, runner, base, network: str):
        super().__init__(runner, addr_key='recoveryVault', base=base, network=network)

class CastsCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('casts', runner, endpoint=ENDPOINTS[network]['aragon_voting'], network=network, pbar_enabled=False)

        @self.postprocessor
        def changeColumnNames(df: pd.DataFrame) -> pd.DataFrame:
            df = df.rename(columns={
                'voterId':'voter', 
                'voteAppAddress':'appAddress',
                'voteOrgAddress':'orgAddress'})
            return df

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.casts(**kwargs).select(
            ds.Cast.id,
            ds.Cast.vote.select(ds.Vote.id),
            ds.Cast.voter.select(ds.Voter.id),
            ds.Cast.supports,
            ds.Cast.stake,
            ds.Cast.createdAt,
            ds.Cast.vote.select(
                ds.Vote.orgAddress,
                ds.Vote.appAddress
            )
        )

class OrganizationsCollector(GraphQLCollector):
    DAO_NAMES=pkgutil.get_data(aragon_module_name, 'dao_names.json')

    def __init__(self, runner, network: str):
        super().__init__('organizations', runner, endpoint=ENDPOINTS[network]['aragon'], network=network)

        @self.postprocessor
        def set_dead_recoveryVault(df: pd.DataFrame) -> pd.DataFrame:
            df['recoveryVault'] = df['recoveryVault'].replace(r'^0x0+$', np.NaN, regex=True)
            return df

        @self.postprocessor
        def apply_names(df: pd.DataFrame) -> pd.DataFrame:
            names_dict = json.loads(self.DAO_NAMES)

            if self.network not in names_dict.keys() or \
            not names_dict[self.network] or \
            df.empty:
                return df

            names_df = pd.json_normalize(names_dict[self.network])
            names_df['id'] = names_df['address'].str.lower()
            names_df['name'] = names_df['name'].fillna(names_df['domain'])
            names_df = names_df[['id', 'name']]
            df = df.merge(names_df, on='id', how='left')

            return df

        @self.postprocessor
        def copy_id(df: pd.DataFrame) -> pd.DataFrame:
            df['orgAddress'] = df['id']
            return df

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.organizations(**kwargs).select(
            ds.Organization.id,
            ds.Organization.createdAt,
            ds.Organization.recoveryVault
        )

class MiniMeTokensCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('miniMeTokens', runner, endpoint=ENDPOINTS[network]['aragon_tokens'], network=network, pbar_enabled=False)

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.miniMeTokens(**kwargs).select(
            ds.MiniMeToken.id,
            ds.MiniMeToken.address,
            ds.MiniMeToken.totalSupply,
            ds.MiniMeToken.transferable,
            ds.MiniMeToken.name,
            ds.MiniMeToken.symbol,
            ds.MiniMeToken.orgAddress,
            ds.MiniMeToken.appAddress,
            ds.MiniMeToken.lastUpdateAt
        )

class TokenHoldersCollector(GraphQLCollector):
    def __init__(self, runner: GraphQLRunner, network: str):
        super().__init__('tokenHolders', runner, endpoint=ENDPOINTS[network]['aragon_tokens'], network=network)

        @self.postprocessor
        def add_minitokens(df: pd.DataFrame) -> pd.DataFrame:
            tokens = runner.filterCollector(name='miniMeTokens', network=network).df
            tokens = tokens.rename(columns={'address':'tokenAddress', 'orgAddress':'organizationAddress'})
            return df.merge(tokens[['tokenAddress', 'organizationAddress']], on='tokenAddress', how='left')
            
    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.tokenHolders(**kwargs).select(
            ds.TokenHolder.id,
            ds.TokenHolder.address,
            ds.TokenHolder.tokenAddress,
            ds.TokenHolder.lastUpdateAt,
            ds.TokenHolder.balance
        )

class TokenPricesCollector(CCPricesCollector):
    pass

class ReposCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('repos', runner, network=network, endpoint=ENDPOINTS[network]['aragon'])

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.repos(**kwargs).select(
            ds.Repo.id,
            ds.Repo.address,
            ds.Repo.name,
            ds.Repo.node,
            ds.Repo.appCount
        )

class TransactionsCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('transactions', runner, network=network, endpoint=ENDPOINTS[network]['aragon_finance'])

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.transactions(**kwargs).select(
            ds.Transaction.id,
            ds.Transaction.orgAddress,
            ds.Transaction.appAddress,
            ds.Transaction.token,
            ds.Transaction.entity,
            ds.Transaction.isIncoming,
            ds.Transaction.amount,
            ds.Transaction.date,
            ds.Transaction.reference
        )

class VotesCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('votes', runner, network=network, endpoint=ENDPOINTS[network]['aragon_voting'])

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.votes(**kwargs).select(
            ds.Vote.id,
            ds.Vote.orgAddress,
            ds.Vote.appAddress,
            ds.Vote.creator,
            ds.Vote.originalCreator,
            ds.Vote.metadata,
            ds.Vote.executed,
            ds.Vote.executedAt,
            ds.Vote.startDate,
            ds.Vote.supportRequiredPct,
            ds.Vote.minAcceptQuorum,
            ds.Vote.yea,
            ds.Vote.nay,
            ds.Vote.voteNum,
            ds.Vote.votingPower
        )

class AragonRunner(GraphQLRunner):
    name: str = 'aragon'

    def __init__(self, dw=None):
        super().__init__(dw)
        self._collectors: List[Collector] = []
        ## TODO: Fix aragon-tokens xdai subgraph and redeploy
        self.networks = ['mainnet']

        for n in self.networks: 
            self._collectors.extend([
                AppsCollector(self, n),
                CastsCollector(self, n),
                MiniMeTokensCollector(self, n),
                ReposCollector(self, n),
                TransactionsCollector(self, n),
                TokenHoldersCollector(self, n),
                VotesCollector(self, n)
            ])
            oc = OrganizationsCollector(self, n)
            bc = BalancesCollector(self, oc, n)
            self._collectors += [oc, bc]
        
        self._collectors.append(CCPricesCollector(self))

    @property
    def collectors(self) -> List[Collector]:
        return self._collectors