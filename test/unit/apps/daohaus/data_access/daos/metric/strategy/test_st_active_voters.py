"""
   Descp: Active voters test.

   Created on: 8-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.\
    st_active_voters import StActiveVoters

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StActiveVotersTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int]) -> None:
        strategy: StActiveVoters = StActiveVoters()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=1, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'memberAddress': 1, 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-3)-01T00:00:00+00:00
            {'memberAddress': 1, 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=25).unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'memberAddress': 1, 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'memberAddress': 2, 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()},#today_year-(today_month-1)-01T23:00:00+00:00
            {'memberAddress': 2, 'trash': 'trash', 'createdAt': bl.sub(month=1).change(minute=59, second=59).unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'memberAddress': 3, 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'memberAddress': 1, 'trash': 'trash', 'createdAt': bl.add(month=2, second=1).change(day=21).unix()},#today_year-today_month-21T00:00:00+00:00
        ])
        out: List[int] = [1, 3, 1, 1]

        self.__check_lists(df=in_df, out=out)


    def test_process_data_repetitions(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=1, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'memberAddress': 1,'createdAt': bl.unix()},#today_year-(today_month-3)-01T00:00:00+00:00
            {'memberAddress': 1,'createdAt': bl.change(day=28).unix()},#today_year-(today_month-3)-28T00:00:00+00:00
            {'memberAddress': 1,'createdAt': bl.unix()},#today_year-(today_month-3)-25T00:00:00+00:00
            {'memberAddress': 1,'createdAt': bl.change(day=6, hour=23).unix()},#today_year-(today_month-3)-06T23:00:00+00:00
        ])
        out: List[int] = [1, 0, 0, 0]

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
