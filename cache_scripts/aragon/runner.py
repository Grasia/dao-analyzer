"""
    Descp: Aragon Runner and Collectors

    Created on: 02-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from typing import List
from gql.dsl import DSLField, DSLSchema

from common import Collector, GraphQLCollector, Runner

class AppsCollector(GraphQLCollector):
    def __init__(self, runner):
        # TODO: Get endpoint
        # TODO: Use networks
        # Two instantiations with different network?
        # One instantiation with multiple networks?
        super().__init__('apps', runner, 'https://api.thegraph.com/subgraphs/name/aragon/aragon-mainnet')

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

class AragonRunner(Runner):
    name: str = 'aragon'

    def __init__(self):
        super().__init__()
        self._collectors: List[Collector] = [
            AppsCollector(self)
        ]

    @property
    def collectors(self):
        return self._collectors