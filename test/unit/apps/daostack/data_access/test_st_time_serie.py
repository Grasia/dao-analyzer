"""
   Descp: Tester for StTimeSerie.

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
from src.apps.daostack.data_access.graphql.dao_stacked_serie.strategy.\
    st_time_serie import StTimeSerie

from src.apps.daostack.business.transfers.stacked_serie import StackedSerie


class StTimeSerieTest(unittest.TestCase):
    def test_get_query_1(self):
        st_ts: StTimeSerie = StTimeSerie(m_type=0)
        query: Query = st_ts.get_query(n_first=100, n_skip=100, o_id='1')
        qb: QueryBuilder = QueryBuilder([query])

        sol: str = "{ reputationHolders(where: {dao: \"1\"}, first: 100, skip: 100, ){ createdAt } }"

        self.assertEqual(sol, qb.build())


    def test_get_query_2(self):
        st_ts: StTimeSerie = StTimeSerie(m_type=1)
        query: Query = st_ts.get_query(n_first=10, n_skip=1, o_id='2')
        qb: QueryBuilder = QueryBuilder([query])

        sol: str = "{ proposals(where: {dao: \"2\"}, first: 10, skip: 1, ){ createdAt } }"

        self.assertEqual(sol, qb.build())


    @given(sol=st.lists(
        st.integers(min_value=0, max_value=5),
        min_size=5,
        max_size=5))
    @settings(max_examples=30)
    def test_process_data(self, sol: List[int]):
        # first element should be at least 1
        if sol[0] == 0:
            sol[0] = 1
        
        df: pd.DataFrame = pd.DataFrame(columns=['date'])
        date = dt.date.today().replace(day=1)
        date = date + relativedelta(months=-4)
        sol_dates: List = list()

        # fill df with repeated dates
        for times in sol:
            unix: int = int(calendar.timegm(date.timetuple()))
            for _ in range(times):
                serie: pd.Series = pd.Series([unix], index=df.columns)
                df = df.append(serie, ignore_index=True)

            sol_dates.append(date.strftime("%d/%m/%Y"))
            date = date + relativedelta(months=+1)

        sserie: StackedSerie = StTimeSerie(0).process_data(df=df)

        # check stacked values
        values = sserie.get_i_stack(0)
        self.assertEqual(len(sol), len(values), sserie.get_serie())
        for i, elem in enumerate(values):
            self.assertEqual(sol[i], elem, f'{sol} != {values}')
        
        # check time serie
        dates_r = sserie.get_serie()
        self.assertEqual(len(sol_dates), len(dates_r))
        for i, date in enumerate(dates_r):
            self.assertEqual(sol_dates[i], date.strftime("%d/%m/%Y"))


if __name__ == "__main__":
    unittest.main()
