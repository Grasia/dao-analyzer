"""
    Descp: Daostack Runner and Collectors

    Created on: 15-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from typing import List, Callable

import pandas as pd
from gql.dsl import DSLField

from .. import config
from ..common.blockscout import BlockscoutBallancesCollector
from ..common.cryptocompare import CCPricesCollector

from ..common import ENDPOINTS, Collector
from ..common.graphql import GraphQLCollector, GraphQLRunner, add_where

def _changeProposalColumnNames(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        'daoId': 'dao',
        'proposalId': 'proposal'
    })
    return df

def _remove_phantom_daos_wr(daoc: 'DaosCollector') -> Callable[[pd.DataFrame], pd.DataFrame]:
    def _remove_phantom_daos(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or daoc.df.empty: 
            return df
        
        return df[df.dao.isin(daoc.df.dao)]
    
    return _remove_phantom_daos

class BalancesCollector(BlockscoutBallancesCollector):
    def __init__(self, runner, base, network: str):
        super().__init__(runner, base=base, network=network, addr_key='dao')

class DaosCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('daos', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        
        @self.postprocessor
        def changeColumnNames(df: pd.DataFrame) -> pd.DataFrame:
            df = df.rename(columns={
                'nativeTokenId':'nativeToken',
                'nativeReputationId':'nativeReputation'})
            return df
        
        @self.postprocessor
        def clone_id(df: pd.DataFrame) -> pd.DataFrame:
            if df.empty:
                return df

            df['dao'] = df['id']
            return df

    def query(self, **kwargs) -> DSLField:
        ds = self.schema

        where = { 'register': 'registered' }
        if config.daostack_all:
            where.pop('register')
        
        return ds.Query.daos(**add_where(kwargs, **where)).select(
            ds.DAO.id,
            ds.DAO.name,
            ds.DAO.register,
            ds.DAO.nativeToken.select(ds.Token.id),
            ds.DAO.nativeReputation.select(ds.Rep.id)
        )

class ProposalsCollector(GraphQLCollector):
    def __init__(self, runner, network: str, daoC: DaosCollector):
        super().__init__('proposals', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])

        @self.postprocessor
        def changeColumnNames(df: pd.DataFrame) -> pd.DataFrame:
            return df.rename(columns={
                'daoId': 'dao',
            }).rename(columns=self._stripGenesis)

        @self.postprocessor
        def deleteColums(df: pd.DataFrame) -> pd.DataFrame:
            return df.drop(columns=['competition'], errors='ignore')

        self.postprocessors.append(_remove_phantom_daos_wr(daoC))

    @staticmethod
    def _stripGenesis(s: str):
        tostrip='genesisProtocolParams'

        if s and len(s) > 1 and s.startswith(tostrip):
            s = s[len(tostrip):]
            return s[0].lower() + s[1:]
        else:
            return s

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.proposals(**kwargs).select(
            ds.Proposal.id,
            ds.Proposal.proposer,
            # enum ProposalState { None, ExpiredInQueue, Executed, Queued, PreBoosted, Boosted, QuietEndingPeriod}
            ds.Proposal.stage,
            ds.Proposal.createdAt,
            ds.Proposal.preBoostedAt,
            ds.Proposal.boostedAt,
            ds.Proposal.quietEndingPeriodBeganAt,
            ds.Proposal.closingAt,
            ds.Proposal.preBoostedClosingAt,
            ds.Proposal.executedAt,
            ds.Proposal.totalRepWhenExecuted,
            ds.Proposal.totalRepWhenCreated,
            ds.Proposal.executionState,
            ds.Proposal.expiresInQueueAt,
            ds.Proposal.votesFor,
            ds.Proposal.votesAgainst,
            ds.Proposal.winningOutcome,
            ds.Proposal.stakesFor,
            ds.Proposal.stakesAgainst,
            ds.Proposal.genesisProtocolParams.select(
                ds.GenesisProtocolParam.queuedVoteRequiredPercentage,
                ds.GenesisProtocolParam.queuedVotePeriodLimit,
                ds.GenesisProtocolParam.boostedVotePeriodLimit,
                # Used for Holografic Consensus threshold
                ds.GenesisProtocolParam.thresholdConst,
                ds.GenesisProtocolParam.minimumDaoBounty,
                ds.GenesisProtocolParam.daoBountyConst,
            ),
            ds.Proposal.dao.select(ds.DAO.id),
            ds.Proposal.competition.select(ds.CompetitionProposal.id)
        )

class ReputationHoldersCollector(GraphQLCollector):
    def __init__(self, runner, network: str, daoC: DaosCollector):
        super().__init__('reputationHolders', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        self.postprocessor(_changeProposalColumnNames)

        self.postprocessors.append(_remove_phantom_daos_wr(daoC))

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.reputationHolders(**kwargs).select(
            ds.ReputationHolder.id,
            ds.ReputationHolder.contract,
            ds.ReputationHolder.address,
            ds.ReputationHolder.balance,
            ds.ReputationHolder.createdAt,
            ds.ReputationHolder.dao.select(ds.DAO.id)
        )

class StakesCollector(GraphQLCollector):
    def __init__(self, runner, network: str, daoC: DaosCollector):
        super().__init__('stakes', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        self.postprocessor(_changeProposalColumnNames)
    
        self.postprocessors.append(_remove_phantom_daos_wr(daoC))

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.proposalStakes(**kwargs).select(
            ds.ProposalStake.id,
            ds.ProposalStake.createdAt,
            ds.ProposalStake.staker,
            ds.ProposalStake.outcome,
            ds.ProposalStake.amount,
            ds.ProposalStake.dao.select(ds.DAO.id),
            ds.ProposalStake.proposal.select(ds.Proposal.id)
        )

class TokenPricesCollector(CCPricesCollector):
    pass

class VotesCollector(GraphQLCollector):
    def __init__(self, runner, network: str, daoC: DaosCollector):
        super().__init__('votes', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        self.postprocessor(_changeProposalColumnNames)

        self.postprocessors.append(_remove_phantom_daos_wr(daoC))

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.proposalVotes(**kwargs).select(
            ds.ProposalVote.id,
            ds.ProposalVote.createdAt,
            ds.ProposalVote.voter,
            ds.ProposalVote.outcome,
            ds.ProposalVote.reputation,
            ds.ProposalVote.dao.select(ds.DAO.id),
            ds.ProposalVote.proposal.select(ds.Proposal.id)
        )

class CommonRepEventCollector(GraphQLCollector):
    def __init__(self, name, runner, base, network: str): 
        super().__init__(name, runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        self.base = base

        @self.postprocessor
        def add_dao_id(df: pd.DataFrame) -> pd.DataFrame:
            """ Using the contract info, appends the DAO id.
            Used by ReputationMintsCollector and ReputationBurnsCollector
            """
            # Skip postprocessor if empty
            if df.empty:
                return df
            
            l_index = ['network', 'contract']
            r_index = ['network', 'nativeReputation']

            wants = ['dao']
            prev_cols = list(df.columns)

            # Add the DAO field to the dataframe
            df = df.merge(self.base.df[r_index + wants],
                how='left',
                left_on=l_index,
                right_on=r_index,
            )

            # Get only the dao field
            df = df[prev_cols + wants]
            
            return df

        self.postprocessors.append(_remove_phantom_daos_wr(self.base))

class ReputationMintsCollector(CommonRepEventCollector):
    def __init__(self, *args, **kwargs):
        super().__init__('reputationMints', *args, **kwargs)

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.reputationMints(**add_where(kwargs, amount_not=0)).select(
            ds.ReputationMint.id,
            # ds.ReputationMint.txHash, # Not used
            ds.ReputationMint.contract,
            ds.ReputationMint.address,
            ds.ReputationMint.amount,
            ds.ReputationMint.createdAt
        )

class ReputationBurnsCollector(CommonRepEventCollector):
    def __init__(self, *args, **kwargs):
        super().__init__('reputationBurns', *args, **kwargs)

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.reputationBurns(**add_where(kwargs, amount_not=0)).select(
            ds.ReputationBurn.id,
            # ds.ReputationBurn.txHash, # Not used
            ds.ReputationBurn.contract,
            ds.ReputationBurn.address,
            ds.ReputationBurn.amount,
            ds.ReputationBurn.createdAt
        )

class DaostackRunner(GraphQLRunner):
    name: str = 'daostack'

    def __init__(self):
        super().__init__()
        self._collectors: List[Collector] = []
        for n in self.networks:
            dc = DaosCollector(self, n)

            self._collectors.extend([
                dc,
                ProposalsCollector(self, n, dc),
                ReputationHoldersCollector(self, n, dc),
                StakesCollector(self, n, dc),
                VotesCollector(self, n, dc),
                BalancesCollector(self, dc, n),
                ReputationMintsCollector(self, dc, n),
                ReputationBurnsCollector(self, dc, n),
            ])

    @property
    def collectors(self) -> List[Collector]:
        return self._collectors
