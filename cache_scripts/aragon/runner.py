"""
    Descp: Aragon Runner and Collectors

    Created on: 02-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from typing import List, Dict
import os

from gql.dsl import DSLField
import pandas as pd
import json

from common import ENDPOINTS, Collector, GraphQLCollector, Runner

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

class CastsCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('casts', runner, endpoint=ENDPOINTS[network]['aragon_voting'], network=network, pbar_enabled=False)

        @self.postprocessor
        def changeColumnNames(df: pd.DataFrame) -> pd.DataFrame:
            df.rename(columns={
                'voterId':'voter', 
                'voteAppAddress':'appAddress',
                'voteOrgAddress':'orgAddress'}, inplace=True)
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
    DAO_NAMES_PATH=os.path.join('cache_scripts', 'aragon', 'dao_names.json')

    def __init__(self, runner, network: str):
        super().__init__('organizations', runner, endpoint=ENDPOINTS[network]['aragon'], network=network)

        @self.postprocessor
        def apply_names(df: pd.DataFrame) -> pd.DataFrame:
            with open(self.DAO_NAMES_PATH, 'r') as f:
                names_dict = json.load(f)

            if self.network not in names_dict.keys() or \
            not names_dict[self.network] or \
            df.empty:
                return df

            names_df = pd.json_normalize(names_dict[self.network])
            names_df['id'] = names_df['address'].str.lower()
            names_df = names_df[['id', 'name']]
            df = df.merge(names_df, on='id', how='left')

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
            ds.MiniMeToken.appAddress
        )

class TokenHoldersCollector(GraphQLCollector):
    ## TODO: Run the n_requests for EACH tokenAddress, with its respective progress and everything
    def __init__(self, runner, network: str):
        super().__init__('tokenHolders', runner, endpoint=ENDPOINTS[network]['aragon_tokens'], network=network)

        @self.postprocessor
        def add_minitokens(df: pd.DataFrame) -> pd.DataFrame:
            ## TODO: Make the runner know that TokenHoldersCollector MUST
            # be run AFTER MiniMeTokensCollector, with some kind of dependency
            # resolving.
            ## TODO: Add some way to get the already instantiated collector from 'runner'
            # instead of creating a new one
            tokens = MiniMeTokensCollector(runner, network).df
            tokens.rename(columns={'address':'tokenAddress', 'orgAddress':'organizationAddress'}, inplace=True)
            return df.merge(tokens[['tokenAddress', 'organizationAddress']], on='tokenAddress', how='left')
            
    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.tokenHolders(**kwargs).select(
            ds.TokenHolder.id,
            ds.TokenHolder.address,
            ds.TokenHolder.tokenAddress,
            ds.TokenHolder.balance
        )

    def transform_to_df(self, data: List[Dict]) -> pd.DataFrame:
        ## TODO: see _tranform_to_df in token_holders.py
        return super().transform_to_df(data)

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
            ds.Vote.metadata,
            ## TODO: Use one of the following fields to implement the database
            # updating mechanism
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

class AragonRunner(Runner):
    name: str = 'aragon'

    def __init__(self):
        super().__init__()
        self._collectors: List[Collector] = []
        ## TODO: More Pythonic way of doing this
        for n in self.networks: 
            self._collectors.extend([
                AppsCollector(self, n),
                CastsCollector(self, n),
                OrganizationsCollector(self, n),
                ReposCollector(self, n),
                TransactionsCollector(self, n),
                VotesCollector(self, n)
            ])
        
        ## TODO: Fix aragon-tokens xdai subgraph and redeploy
        self._collectors.append(MiniMeTokensCollector(self, 'mainnet'))
        self._collectors.append(TokenHoldersCollector(self, 'mainnet'))

    @property
    def collectors(self) -> List[Collector]:
        return self._collectors