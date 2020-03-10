"""
   Descp: Tester for query builder.

   Created on: 10-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import unittest
from hypothesis import given, example

from src.api.query import Query
from src.api.query_builder import QueryBuilder

class QueryBuilderTest(unittest.TestCase):
    
    #@example(None)
    #@example([Query()])
    def test_build(self, queries = None):
        builder: QueryBuilder = QueryBuilder(None)
        self.assertEqual(builder.build(), '{}')



if __name__ == "__main__":
    unittest.main()