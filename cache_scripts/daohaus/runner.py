"""
    Descp: Daohaus Runner and Collectors

    Created on: 13-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
import requests
from typing import List

import pandas as pd
from tqdm import tqdm
from gql.dsl import DSLField

import config
from common import ENDPOINTS, Collector, GraphQLCollector, Runner, add_where

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
        def moloch_names(df: pd.DataFrame) -> pd.DataFrame:
            # TODO: Run only when they don't have already a name
            # TODO: Paralelizing somehow?
            df = df.rename(columns={"title":"name"})
            if not config.skip_daohaus_names:
                tqdm.pandas(desc="Getting moloch names")
                df["name"] = df.progress_apply(lambda x:self._request_moloch_name(x['id']), axis=1)
            return df
    
    @staticmethod
    def _request_moloch_name(moloch_id: str):
        response = requests.get(DATA_ENDPOINT.format(id=moloch_id))

        o = response.json()
        if isinstance(o, list) and o and "name" in o[0]:
            return o[0]["name"]
        else:
            return None
    
    def query(self, **kwargs) -> DSLField:
        ds = self.schema
        # FIXME: There are lots of fields that have changed
        # TODO: Implement some way to skip verification
        return ds.Query.moloches(**add_where(kwargs, deleted=False)).select(
            ds.Moloch.id,
            ds.Moloch.title, # TODO: Research this
            ds.Moloch.version,
            ds.Moloch.summoner,
            ds.Moloch.summoningTime,
            ds.Moloch.timestamp, # TODO: Research this
            ds.Moloch.proposalCount, # TODO: Research this
            ds.Moloch.memberCount, # TODO: Research this
            ds.Moloch.voteCount, # TODO: Research this
            ds.Moloch.rageQuitCount, # TODO: Research this
            ds.Moloch.totalGas # TODO: Research this
        )

class ProposalsCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('proposals', runner, network=network, endpoint=ENDPOINTS[network]["daohaus"])

        # TODO: Add a way of updating (see _get_open_proposals)

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
            ds.Proposal.didPass,
            ds.Proposal.yesShares,
            ds.Proposal.noShares
        )

class RageQuitCollector(GraphQLCollector):
    def __init__(self, runner, network: str):
        super().__init__('rageQuits', runner, network=network, endpoint=ENDPOINTS[network]["daohaus"])
        # TODO: See update_rage_quits...

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

class DaohausRunner(Runner):
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
                VoteCollector(self, n)
            ])

    @property
    def collectors(self) -> List[Collector]:
        return self._collectors