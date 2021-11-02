"""
    Descp: Aragon Runner and Collectors

    Created on: 02-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from gql.dsl import DSLField, DSLSchema

from cache_scripts.common import GraphQLCollector, Runner

class AppsCollector(GraphQLCollector):
    def __init__(self, runner):
        super().__init__(self, 'apps', runner, endpoint)

    @staticmethod
    def build_query(ds: DSLSchema, **kwargs) -> DSLField:
        return ds.Query.apps(**kwargs).select(
            ds.app.id,
            ds.app.isForwarder,
            ds.app.isUpgradeable,
            ds.app.repoName,
            ds.app.repoAddress,
            ds.app.organization.select(ds.Organization.id)
        )

class AragonRunner(Runner):
    def __init__(self):
        super().__init__(self, 'aragon')
        self.collectors = [
        ]