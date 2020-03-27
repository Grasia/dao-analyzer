"""
   Descp: Tester for StProposalOutcome.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
from hypothesis import given, settings, strategies as st
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar

from src.api.graphql.query import Query
from src.api.graphql.query_builder import QueryBuilder
import src.apps.daostack.data_access.graphql.dao_metric.strategy.\
    st_proposal_outcome as st_po

from src.apps.daostack.business.transfers.stacked_serie import StackedSerie


StIntList = st.lists(
                st.integers(min_value=0, max_value=5),
                min_size=5,
                max_size=5)

StBoolList = st.lists(
                st.booleans(),
                min_size=5,
                max_size=5)


class StProposalOutcomeTest(unittest.TestCase):
    def test_get_query(self):
        st: st_po.StProposalOutcome = st_po.StProposalOutcome(
            st_po.BOOST_OUTCOME)
        query: Query = st.get_query(n_first=100, n_skip=100, o_id='1')
        qb: QueryBuilder = QueryBuilder([query])

        sol: str = "{ proposals(where: {dao: \"1\", executedAt_not: null}, first: 100, skip: 100,\
 ){ executedAt executionState winningOutcome } }"

        self.assertEqual(sol, qb.build())


    @given(n_dates=StIntList, passed=StBoolList, boost=StBoolList)# noqa: C901
    @settings(max_examples=30)
    def test_process_data(self, n_dates, passed, boost):
        # first element must be at least 1
        if n_dates[0] == 0:
            n_dates[0] = 1
        
        df: pd.DataFrame = pd.DataFrame(columns=['closedAt', 'hasPassed', 
            'isBoosted'])
        date = dt.date.today().replace(day=1)
        date = date + relativedelta(months=-4)
        sol_dates: List = list()

        # fill df with repeated dates
        for i, times in enumerate(n_dates):
            unix: int = int(calendar.timegm(date.timetuple()))
            for _ in range(times):
                serie: pd.Series = pd.Series([unix, passed[i], boost[i]],
                    index=df.columns)
                df = df.append(serie, ignore_index=True)

            sol_dates.append(date.strftime("%d/%m/%Y"))
            date = date + relativedelta(months=+1)

        sserie: StackedSerie = st_po.StProposalOutcome(
            st_po.BOOST_OUTCOME).process_data(df=df)

        # check time serie
        dates_r = sserie.get_serie()
        self.assertEqual(len(sol_dates), len(dates_r))
        for i, date in enumerate(dates_r):
            self.assertEqual(sol_dates[i], date.strftime("%d/%m/%Y"))

        # check stacked values
        stacks = sserie.get_stacks()
        for j, stack in enumerate(stacks):
            for i, x in enumerate(stack):
                # absolute majority pass
                if j == 0 and passed[i] and not boost[i]:
                    self.assertEqual(x, n_dates[i])
                # relative majority pass
                elif j == 1 and passed[i] and boost[i]:
                    self.assertEqual(x, n_dates[i])
                # relative majority fail
                elif j == 2 and not passed[i] and boost[i]:
                    self.assertEqual(x, n_dates[i])
                # absolute majority fail
                elif j == 3 and not passed[i] and not boost[i]:
                    self.assertEqual(x, n_dates[i])
                else:
                    self.assertEqual(x, 0)

if __name__ == "__main__":
    unittest.main()
