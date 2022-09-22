"""
   Descp: Tester of percentage of holders who vote.

   Created on: 05-nov-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.\
    st_total_members import StTotalMembers 
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StVotersPercentageTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int], stype: int) -> None:
        strategy: StTotalMembers = StTotalMembers()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_same_size(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'exists': True, 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'createdAt': bl.change(second=59, minute=59).unix()}, #today_year-(today_month-1)-01T23:59:00+00:00
            {'exists': True, 'createdAt': bl.add(month=1).unix()}, #today_year-today_month-01T23:59:59+00:00
            {'exists': True, 'createdAt': bl.change(day=21, hour=0).unix()}, #today_year-today_month-21T00:59:00+00:00
        ])
        out: List[int] = [0, -2, 0]

        self.__check_lists(df=in_df, out=out, stype=0)


    def test_news_bigger_size(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'exists': True, 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'exists': True, 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'exists': True, 'createdAt': bl.change(second=59, minute=59).unix()}, #today_year-(today_month-1)-01T23:59:00+00:00
            {'exists': True, 'createdAt': bl.add(month=1).unix()}, #today_year-today_month-01T23:59:59+00:00
            {'exists': True, 'createdAt': bl.change(day=21, hour=0).unix()}, #today_year-today_month-21T00:59:00+00:00
        ])
        out: List[int] = [2, 2, 4]

        self.__check_lists(df=in_df, out=out, stype=0)


    def test_outs_bigger_size(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'createdAt': bl.change(second=59, minute=59).unix()}, #today_year-(today_month-1)-01T23:59:00+00:00
            {'createdAt': bl.add(month=1).unix()}, #today_year-today_month-01T23:59:59+00:00
            {'createdAt': bl.change(day=21, hour=0).unix()}, #today_year-today_month-21T00:59:00+00:00
        ])
        out: List[int] = [-2, -4, -6]

        self.__check_lists(df=in_df, out=out, stype=0)


if __name__ == "__main__":
    unittest.main()
