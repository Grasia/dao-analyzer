"""
    Descp: Daohaus Runner and Collectors

    Created on: 13-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
import requests
import requests_cache
from typing import List

import pandas as pd
from tqdm import tqdm
from gql.dsl import DSLField

import config
from metadata import Block
from common import ENDPOINTS, Collector, GraphQLCollector, GraphQLUpdatableCollector, GraphQLRunner, add_where, partial_query

DATA_ENDPOINT: str = "https://data.daohaus.club/dao/{id}"

class MembersCollector(GraphQLUpdatableCollector):
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
                cached = requests_cache.CachedSession(self.data_path.parent / '.names_cache', use_cache_dir=False)
                tqdm.pandas(desc="Getting moloch names")
                df["name"] = df.progress_apply(lambda x:self._request_moloch_name(x['id'], req=cached), axis=1)
            return df
    
    @staticmethod
    def _request_moloch_name(moloch_id: str, req=None):
        # TODO: Cache names somehow
        if req is None:
            req = requests
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
            ds.Moloch.timestamp, # TODO: What's this?
            ds.Moloch.proposalCount,
            ds.Moloch.memberCount,
            ds.Moloch.voteCount,
            ds.Moloch.rageQuitCount,
            ds.Moloch.totalGas
        )

class ProposalsCollector(GraphQLUpdatableCollector):
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
    
    def update(self, block: Block = None):
        # Getting recently processed proposals
        self._simple_timestamp('processedAt', block,
            start_txt='Getting recently processed proposals since {date}',
            end_txt='{len} proposals have been processed'
        )

        # Getting still open proposals which counts could have been updated
        # If they are not sponsored, they won't change
        data = self.requester.n_requests(
            query=partial_query(self.query, {"processed": False, "sponsored": False}),
            block_hash=block.id
        )
        df = self.transform_to_df(data)
        self._update_data(df)

        # Getting recently created Proposals
        # Some of them could be unsponsored and remain there, which is why they
        # would not be requested in the "still open proposals" request above
        self._simple_timestamp('createdAt', block,
            start_txt='Getting recently created proposals since {date}',
            end_txt='{len} proposals have been created'
        )

class RageQuitCollector(GraphQLUpdatableCollector):
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

class VoteCollector(GraphQLUpdatableCollector):
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
                VoteCollector(self, n)
            ])

    @property
    def collectors(self) -> List[Collector]:
        return self._collectors