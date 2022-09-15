"""
   Descp: This class is used to build a GraphQL query.

   Created on: 26-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List

from dao_analyzer.web.apps.common.api.graphql.query import Query

class QueryBuilder():

    def __init__(self, queries: List[Query] = None):
        self.queries: List[Query] = queries if queries else list()


    def add_query(self, query: Query):
        self.queries.append(query)


    def build(self) -> str:
        query: str = '{ '
        
        for q in self.queries:
            q_filter: str = ''
            for f in q.filters:
                q_filter += f'{f}: {q.filters[f]}, '

            q_body: str = ''
            if type(q.body) == list:
                q_body += '{ '
                for attr in q.body:
                    q_body += f'{attr} '
                q_body += '}'

            elif type(q.body) == Query:
                q_builder: QueryBuilder = QueryBuilder([q.body])
                q_body += q_builder.build()

            query += f'{q.header}({q_filter}){q_body} '

        query += '}'
        return query