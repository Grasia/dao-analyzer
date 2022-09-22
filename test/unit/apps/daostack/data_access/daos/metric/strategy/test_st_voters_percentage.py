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
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_voters_percentage import StVotersPercentage
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StVotersPercentageTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[float], stype: int) -> None:
        strategy: StVotersPercentage = StVotersPercentage()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_same_size(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'voter': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.change(second=59, minute=59).unix()}, #today_year-(today_month-1)-01T23:59:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.add(month=1).unix()}, #today_year-today_month-01T23:59:59+00:00
            {'trash': 'trash', 'createdAt': bl.change(day=21, hour=0).unix()}, #today_year-today_month-21T00:59:00+00:00
        ])
        out: List[float] = [100.0, 50.0, 33.3333]

        self.__check_lists(df=in_df, out=out, stype=0)


    def test_holders_bigger_size(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'voter': '0', 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.change(second=59, minute=59).unix()}, #today_year-(today_month-1)-01T23:59:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.add(month=1).unix()}, #today_year-today_month-01T23:59:59+00:00
            {'trash': 'trash', 'createdAt': bl.change(day=21, hour=0).unix()}, #today_year-today_month-21T00:59:00+00:00
        ])
        out: List[float] = [0.0, 100.0, 33.3333]

        self.__check_lists(df=in_df, out=out, stype=0)


    def test_voters_bigger_size(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'voter': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'voter': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.change(second=59, minute=59).unix()}, #today_year-(today_month-1)-01T23:59:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.add(month=1).unix()}, #today_year-today_month-01T23:59:59+00:00
            {'trash': 'trash', 'createdAt': bl.change(day=21, hour=0).unix()}, #today_year-today_month-21T00:59:00+00:00
        ])
        out: List[float] = [None, 100.0, 50.0]

        self.__check_lists(df=in_df, out=out, stype=0)


if __name__ == "__main__":
    unittest.main()
