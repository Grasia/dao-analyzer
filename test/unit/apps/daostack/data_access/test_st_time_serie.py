"""
   Descp: Tester for StTimeSerie.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from hypothesis import given, settings, strategies as st
from typing import List, Dict

from src.api.graphql.query import Query
from src.api.graphql.query_builder import QueryBuilder
from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
    st_time_serie import StTimeSerie


class StTimeSerieTest(unittest.TestCase):
    def test_get_query_1(self):
        st_ts: StTimeSerie = StTimeSerie(m_type=0)
        query: Query = st_ts.get_query(n_first=100, n_skip=100, o_id='1')
        qb: QueryBuilder = QueryBuilder([query])

        sol: str = "{ dao(id: \"1\", ){ reputationHolders(first: 100, skip: 100, ){ createdAt } } }"

        self.assertEqual(sol, qb.build())


    def test_get_query_2(self):
        st_ts: StTimeSerie = StTimeSerie(m_type=1)
        query: Query = st_ts.get_query(n_first=10, n_skip=1, o_id='2')
        qb: QueryBuilder = QueryBuilder([query])

        sol: str = "{ dao(id: \"2\", ){ proposals(first: 10, skip: 1, ){ createdAt } } }"

        self.assertEqual(sol, qb.build())


    def test_process_data(self):
        pass


if __name__ == "__main__":
    unittest.main()
