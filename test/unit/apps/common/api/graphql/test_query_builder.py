"""
   Descp: Tester for query builder.

   Created on: 10-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import List
import unittest
from hypothesis import given, example, settings, strategies as st

from dao_analyzer.web.apps.common.api.graphql.query import Query
from dao_analyzer.web.apps.common.api.graphql.query_builder import QueryBuilder

QueryStrategy = st.builds(
                    Query, 
                    st.text(),
                    st.lists(st.text()),
                    st.dictionaries(
                        keys=st.text(),
                        values=st.text()))


# @st.composite
# def recursive_query(draw) -> Query:
#     return Query(
#         draw(st.text(max_size=10)),
#         draw(QueryStrategy),
#         st.dictionaries(
#             keys=st.text(max_size=10),
#             values=st.text(max_size=10),
#             max_size=10))


class QueryBuilderTest(unittest.TestCase):
    
    @example(queries=None)
    @given(queries=st.lists(QueryStrategy))
    @settings(max_examples=30)
    def test_build_1(self, queries: List[Query]):
        builder: QueryBuilder = QueryBuilder(queries=queries)
        query: str = builder.build()

        # Test that every query has at least curly braces.
        self.assertEqual(f'{query[0]}{query[-1]}', '{}')
        # Test that whether there's at least one query, the string length is
        #  bigger than the first query's header.
        if queries:
            # +2 'cause at least 2 curly braces.
            self.assertGreaterEqual(len(query), len(queries[0].header) + 2)


    def test_build_2(self):
        query1: Query = Query(
                            header='test1',
                            body=['param1', 'param2'],
                            filters={'filt1': 'true', 'filt2': 'false'})
        query2: Query = Query(
                            header='test2',
                            body=Query(
                                header='test3',
                                body=['p1', 'p2'],
                                filters={}
                            ),
                            filters={'f3': True})

        builder: QueryBuilder = QueryBuilder([query1])
        builder.add_query(query2)
        result: str = builder.build()

        sol: str = "{ test1(filt1: true, filt2: false, ){ param1 param2 } \
test2(f3: True, ){ test3(){ p1 p2 } } }"

        self.assertEqual(sol, result, f'Expected = \n{sol}\n found = \n{result}')


if __name__ == "__main__":
    unittest.main()
