"""
   Descp: This is a dao (data access object) of the organization.
    It's used in order to warp the transformation among
    API's responses and the App's transfer.  

   Created on: 24-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import Dict

from src.apps.daostack.business.transfers.organization import Organization
from src.apps.daostack.business.transfers.organization import OrganizationList
from src.apps.api.graphql.query_builder import QueryBuilder
from src.apps.api.graphql.query import Query


class DaoOrganizationList:
    def __init__(self, requester):
        self.__requester = requester


    def __get_query(self, n_first: int, n_skip: int):
        return Query(
                    header = 'daos', 
                    body = ['id', 'name'], 
                    filters = {
                        'where': '{register: \"registered\"}',
                        'first': f'{n_first}',
                        'skip': f'{n_skip}',
                    })


    def get_organizations(self) -> OrganizationList:
        orgs: OrganizationList = OrganizationList()
        chunk: int = 0
        result: Dict = dict()
        condition: bool = True

        while condition:
            e_chunk: int = self.__requester.get_elems_per_chunk(chunk)
            query: Query = self.__get_query(
                                    n_first=e_chunk, 
                                    n_skip=orgs.get_size())
            q_builder: QueryBuilder = QueryBuilder([query])

            result = self.__requester.request(q_builder.build())
            result = result['daos']
        
            for org in result:
                orgs.add_organization(Organization(
                                        o_id=org['id'], 
                                        name=org['name']))

            # means there's still data to request
            condition = len(result) == e_chunk
            chunk += 1
        
        return orgs
