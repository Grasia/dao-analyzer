"""
   Descp: Tester for active organization strategy.

   Created on: 23-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_active_organization import StActiveOrganization
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StActiveOrganizationTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int]) -> None:
        strategy: StActiveOrganization = StActiveOrganization()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'dao': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'dao': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'dao': '0', 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'dao': '1', 'trash': 'trash', 'createdAt': bl.sub(month=1).change(minute=59, second=59).unix()}, #today_year-(today_month-2)-01T23:59:59+00:00
            {'dao': '1', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-01T23:59:59+00:00
            {'dao': '3', 'trash': 'trash', 'createdAt': bl.add(month=2).change(day=15, hour=0).unix()}, #today_year-today_month-15T00:00:00+00:00
            {'dao': '2', 'trash': 'trash', 'createdAt': bl.change(day=21).unix()}, #today_year-today_month-21T00:00:00+00:00
            {'dao': '3', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-today_month-21T00:00:00+00:00
        ])
        out: List[int] = [2, 1, 2]

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
