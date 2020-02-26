"""
   Descp: This class is used to build a GraphQL query.

   Created on: 26-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from api.query import Query

class QueryBuilder():

    def __init__(self):
        self.queries: List[Query] = list()


    def add_query(self, query: Query):
        self.queries.append(query)


    def build(self) -> str:
        query: str = '{'
        
        for q in self.queries:
            q_filter: str = ''
            for f in q.filters:
                q_filter += f'{f}: {q.filters[f]}, '

            # TODO: neasted queries
            q_body: str = ''
            for attr in q.body:
                q_body += f'{attr} '

            query += f'{q.header}({q_filter}){{{q_body}}} '

        query += '}'
        return query