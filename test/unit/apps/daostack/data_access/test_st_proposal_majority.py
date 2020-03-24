"""
   Descp: Test for StProposalMajority class

   Created on: 20-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest

from src.api.graphql.query import Query
from src.api.graphql.query_builder import QueryBuilder
from src.apps.daostack.data_access.graphql.dao_metric.strategy.\
    st_proposal_majority import StProposalMajority


class StProposalMajorityTest(unittest.TestCase):
    def test_get_query(self):
        st: StProposalMajority = StProposalMajority()
        query: Query = st.get_query(n_first=100, n_skip=100, o_id='1')
        qb: QueryBuilder = QueryBuilder([query])

        sol: str = "{ proposals(where: {dao: \"1\", executedAt_not: null}, \
first: 100, skip: 100, ){ executedAt winningOutcome totalRepWhenExecuted \
votesFor votesAgainst genesisProtocolParams{queuedVoteRequiredPercentage} } }"

        self.assertEqual(sol, qb.build())


if __name__ == "__main__":
    unittest.main()
