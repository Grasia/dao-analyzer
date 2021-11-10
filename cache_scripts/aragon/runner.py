"""
    Descp: Aragon Runner and Collectors

    Created on: 02-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from typing import List
from gql.dsl import DSLField

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

class AragonRunner(Runner):
    name: str = 'aragon'

    def __init__(self):
        super().__init__()
        self._collectors: List[Collector] = []
        ## TODO: More Pythonic way of doing this
        for n in self.networks: 
            self._collectors.extend([
                AppsCollector(self, n),
                CastsCollector(self, n)
            ])

    @property
    def collectors(self):
        return self._collectors