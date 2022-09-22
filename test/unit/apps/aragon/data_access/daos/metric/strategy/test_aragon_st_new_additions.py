"""
   Descp: New additions test.

   Created on: 19-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.aragon.data_access.daos.metric.strategy.\
    st_new_additions import StNewAdditions

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StNewMembersTest(unittest.TestCase):

    def test_vote_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=1, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'trash': 'trash', 'startDate': bl.unix()},#today_year-(today_month-3)-01T00:00:00+00:00
            {'trash': 'trash', 'startDate': bl.add(month=1).change(day=25).unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'trash': 'trash', 'startDate': bl.unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'trash': 'trash', 'startDate': bl.add(month=1).change(day=1, hour=23).unix()},#today_year-(today_month-1)-01T23:00:00+00:00
            {'trash': 'trash', 'startDate': bl.sub(month=1).change(minute=59, second=59).unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'trash': 'trash', 'startDate': bl.unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'trash': 'trash', 'startDate': bl.add(month=2, second=1).change(day=21).unix()},#today_year-today_month-21T00:00:00+00:00
        ])
        strategy: StNewAdditions = StNewAdditions(typ=StNewAdditions.VOTE)
        result: StackedSerie = strategy.process_data(df=in_df)
        out: List[int] = [1, 4, 1, 1]

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_transactons_members_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=4, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'date': bl.unix()},#today_year-(today_month-3)-04T00:00:00+00:00
            {'date': bl.add(month=1).change(day=16).unix()},#today_year-(today_month-2)-16T00:00:00+00:00
            {'date': bl.unix()},#today_year-(today_month-2)-16T00:00:00+00:00
            {'date': bl.change(day=9, hour=23).unix()},#today_year-(today_month-2)-09T23:00:00+00:00
            {'date': bl.sub(month=1).change(minute=59, second=59).unix()},#today_year-(today_month-3)-01T23:59:59+00:00
        ])
        strategy: StNewAdditions = StNewAdditions(typ=StNewAdditions.TRANSACTION)
        result: StackedSerie = strategy.process_data(df=in_df)
        out: List[int] = [2, 3, 0, 0]

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


if __name__ == "__main__":
    unittest.main()
