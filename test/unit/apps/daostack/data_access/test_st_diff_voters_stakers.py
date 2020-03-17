"""
   Descp: Tester for StDifferentVS.

   Created on: 17-mar-2020

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
from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
    st_different_voters_stakers import StDifferentVS

from src.apps.daostack.business.transfers.stacked_serie import StackedSerie


StrategyUsers = st.lists(
    st.lists(
        st.fixed_dictionaries({
            'id': st.uuids(),
            'actions': st.integers(min_value=1, max_value=5),
        }),
        min_size=5,
        max_size=5,
    ),
    min_size=5,
    max_size=5)


class StDifferentVSTest(unittest.TestCase):
    def test_get_query_1(self):
        st_ts: StDifferentVS = StDifferentVS(m_type=0)
        query: Query = st_ts.get_query(n_first=100, n_skip=100, o_id='1')
        qb: QueryBuilder = QueryBuilder([query])

        sol: str = "{ proposalVotes(where: {dao: \"1\"}, first: 100, skip: 100, ){ createdAt voter } }"

        self.assertEqual(sol, qb.build())


    def test_get_query_2(self):
        st_ts: StDifferentVS = StDifferentVS(m_type=1)
        query: Query = st_ts.get_query(n_first=10, n_skip=1, o_id='2')
        qb: QueryBuilder = QueryBuilder([query])

        sol: str = "{ proposalStakes(where: {dao: \"2\"}, first: 10, skip: 1, ){ createdAt staker } }"

        self.assertEqual(sol, qb.build())


    @given(
        n_dates=st.integers(min_value=0, max_value=5),
        users=StrategyUsers)
    @settings(max_examples=30)
    def test_process_data(self, n_dates: int, users: List[int]):
        df: pd.DataFrame = pd.DataFrame(columns=['createdAt', 'userId'])
        date = dt.date.today().replace(day=1)
        date = date + relativedelta(months=-(n_dates-1))
        sol_dates: List = list()
        sol_users: List[int] = list()

        # fill df with dates-ids
        for i in range(n_dates):
            unix: int = int(calendar.timegm(date.timetuple()))
            for u in users[i]:
                dates: List = [unix] * u['actions']
                ids: List = [str(u['id'])] * u['actions']
                data = {'createdAt': dates, 'userId': ids}
                df = df.append(pd.DataFrame(data), ignore_index=True)

            sol_users.append(len(users[i]))
            sol_dates.append(date.strftime("%d/%m/%Y"))
            date = date + relativedelta(months=+1)

        sserie: StackedSerie = StDifferentVS(0).process_data(df=df)

        # check calculated values
        values = sserie.get_i_stack(0)
        self.assertEqual(len(sol_users), len(values), sserie.get_serie())

        for i, elem in enumerate(values):
            self.assertEqual(sol_users[i], elem, f'{sol_users} != {values}')
        
        # check calculated dates
        dates_r = sserie.get_serie()
        self.assertEqual(len(sol_dates), len(dates_r))

        for i, date in enumerate(dates_r):
            d = date.strftime("%d/%m/%Y")
            self.assertEqual(sol_dates[i], d, f'{sol_dates} != {dates_r}')


if __name__ == "__main__":
    unittest.main()
