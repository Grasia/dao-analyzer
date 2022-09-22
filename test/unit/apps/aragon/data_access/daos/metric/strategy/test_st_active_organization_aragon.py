"""
   Descp: Active organization test.

   Created on: 23-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.aragon.data_access.daos.metric.strategy.\
    st_active_organization import StActiveOrganization

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StActiveOrganizationTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int]) -> None:
        strategy: StActiveOrganization = StActiveOrganization()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=27, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'orgAddress': 1, 'trash': 'trash', 'createdAt': bl.unix()},#today_year-(today_month-3)-27T00:00:00+00:00
            {'orgAddress': 1, 'trash': 'trash', 'createdAt': bl.change(hour=5).unix()},#today_year-(today_month-3)-27T05:00:00+00:00
            {'orgAddress': 1, 'trash': 'trash', 'date': bl.add(month=2).unix()},#today_year-(today_month-1)-27T05:00:00+00:00
            {'orgAddress': 2, 'trash': 'trash', 'date': bl.change(day=3, hour=23).unix()},#today_year-(today_month-1)-03T23:00:00+00:00
            {'orgAddress': 2, 'trash': 'trash', 'startDate': bl.add(month=1).change(minute=59, second=59).unix()},#today_year-today_month-03T23:59:59+00:00
            {'orgAddress': 3, 'trash': 'trash', 'date': bl.unix()},#today_year-today_month-03T23:59:59+00:00
            {'orgAddress': 2, 'trash': 'trash', 'startDate': bl.add(second=1).change(day=7, hour=17).unix()},#today_year-today_month-07T17:00:00+00:00
        ])
        out: List[int] = [1, 0, 2, 2]

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
