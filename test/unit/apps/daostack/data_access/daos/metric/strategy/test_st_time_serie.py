"""
   Descp: Tester for StTimeSerie.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_time_serie import StTimeSerie

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StTimeSerieTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int]) -> None:
        # m_type it not used, in the future -1 will break it
        strategy: StTimeSerie = StTimeSerie(m_type=-1)
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=1, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'id': '-1', 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-3)-01T00:00:00+00:00
            {'id': '3', 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=25).unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'id': '0', 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'id': '0', 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()},#today_year-(today_month-1)-01T23:00:00+00:00
            {'id': '1', 'trash': 'trash', 'createdAt': bl.sub(month=1).change(minute=59, second=59).unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'id': '1', 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'id': '2', 'trash': 'trash', 'createdAt': bl.add(month=2, second=1).change(day=21).unix()},#today_year-today_month-21T00:00:00+00:00
        ])

        out: List[int] = [1, 4, 1, 1]

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
