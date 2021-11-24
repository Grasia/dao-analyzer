"""
    Descp: Daostack Runner and Collectors

    Created on: 15-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from typing import List

import pandas as pd
from gql.dsl import DSLField

from common import ENDPOINTS, Collector, GraphQLCollector, GraphQLRunner, add_where

def _changeProposalColumnNames(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(columns={
        'daoId': 'dao',
        'proposalId': 'proposal'
    }, inplace=True)
    return df

class DaosCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('daos', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        
        @self.postprocessor
        def changeColumnNames(df: pd.DataFrame) -> pd.DataFrame:
            df.rename(columns={
                'nativeTokenId':'nativeToken',
                'nativeReputationId':'nativeReputation'},inplace=True)
            return df

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.daos(**add_where(kwargs, register="registered")).select(
            ds.DAO.id,
            ds.DAO.name,
            ds.DAO.nativeToken.select(ds.Token.id),
            ds.DAO.nativeReputation.select(ds.Rep.id)
        )

class ProposalsCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('proposals', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])

        ## TODO: If we implement the "continue method"
        # see the _request_open_proposals from proposal_collector.py

        @self.postprocessor
        def changeColumnNames(df: pd.DataFrame) -> pd.DataFrame:
            return df.rename(columns={
                'daoId': 'dao',
                'genesisProtocolParamsQueuedVoteRequiredPercentage': 'queuedVoteRequiredPercentage'
            })

    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        return ds.Query.proposals(**kwargs).select(
            ds.Proposal.id,
            ds.Proposal.proposer,
            ds.Proposal.stage,
            ds.Proposal.createdAt,
            ds.Proposal.preBoostedAt,
            ds.Proposal.boostedAt,
            ds.Proposal.closingAt,
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
            ds.Proposal.genesisProtocolParams.select(ds.GenesisProtocolParam.queuedVoteRequiredPercentage),
            ds.Proposal.dao.select(ds.DAO.id)
        )

class ReputationHoldersCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('reputationHolders', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        self.postprocessor(_changeProposalColumnNames)

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
    def __init__(self, runner, network: str):
        super().__init__('stakes', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        self.postprocessor(_changeProposalColumnNames)
    
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

class VotesCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('votes', runner, network=network, endpoint=ENDPOINTS[network]['daostack'])
        self.postprocessor(_changeProposalColumnNames)

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

class DaostackRunner(GraphQLRunner):
    name: str = 'daostack'

    def __init__(self):
        super().__init__()
        self._collectors: List[Collector] = []
        for n in self.networks:
            self._collectors.extend([
                DaosCollector(self, n),
                ProposalsCollector(self, n),
                ReputationHoldersCollector(self, n),
                StakesCollector(self, n),
                VotesCollector(self, n)
            ])

    @property
    def collectors(self) -> List[Collector]:
        return self._collectors
