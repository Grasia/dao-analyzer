"""
   Descp: New members test.

   Created on: 7-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from src.apps.daohaus.data_access.daos.metric.strategy.\
    st_new_members import StNewMembers

from src.apps.common.business.transfers.stacked_serie import StackedSerie


class StNewMembersTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int]) -> None:
        strategy: StNewMembers = StNewMembers()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=1, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'exists': True, 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-3)-01T00:00:00+00:00
            {'exists': True, 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=25).unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'exists': False, 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'exists': False, 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()},#today_year-(today_month-1)-01T23:00:00+00:00
            {'exists': True, 'trash': 'trash', 'createdAt': bl.sub(month=1).change(minute=59, second=59).unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'exists': True, 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'exists': True, 'trash': 'trash', 'createdAt': bl.add(month=2, second=1).change(day=31).unix()},#today_year-today_month-31T00:00:00+00:00
        ])

        out: List[int] = [1, 3, 0, 1]

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
