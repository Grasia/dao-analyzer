"""
   Descp: Tester for StActiveUsers.

   Created on: 24-aug-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_active_users import StActiveUsers
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StActiveUsersTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int]) -> None:
        strategy: StActiveUsers = StActiveUsers()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'voter': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'proposer': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'staker': '0', 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.sub(month=1).change(minute=59, second=59).unix()}, #today_year-(today_month-2)-01T23:59:59+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-01T23:59:59+00:00
            {'proposer': '3', 'trash': 'trash', 'createdAt': bl.add(month=2).change(day=15, hour=0).unix()}, #today_year-today_month-15T00:00:00+00:00
            {'voter': '2', 'trash': 'trash', 'createdAt': bl.change(day=21).unix()}, #today_year-today_month-21T00:00:00+00:00
            {'staker': '3', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-today_month-21T00:00:00+00:00
        ])
        out: List[int] = [2, 1, 2]

        self.__check_lists(df=in_df, out=out)

        
    def test_process_data_stakers(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'staker': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-3)-25T00:00:00+00:00
            {'staker': '1', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-3)-25T00:00:00+00:00
            {'staker': '1', 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-2)-01T23:00:00+00:00
            {'staker': '2', 'trash': 'trash', 'createdAt': bl.sub(month=1).change(minute=59, second=59).unix()}, #today_year-(today_month-3)-01T23:59:59+00:00
            {'staker': '2', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-3)-01T23:59:59+00:00
            {'staker': '3', 'trash': 'trash', 'createdAt': bl.add(month=3).change(day=2, hour=0, minute=0, second=0).unix()}, #today_year-today_month-02T00:00:00+00:00
        ])
        out: List[int] = [3, 1, 0, 1]

        self.__check_lists(df=in_df, out=out)


    def test_process_data_non_id(self):
        in_df: pd.DataFrame = pd.DataFrame([
            {'createdAt': 1571961600, 'proposer': None, 'trash': 'trash'},
            {'createdAt': 1571961600, 'proposer': None, 'trash': 'trash'},
            {'createdAt': 1572649200, 'proposer': None, 'trash': 'trash'},
            {'createdAt': 1569974399, 'proposer': None, 'trash': 'trash'},
            {'createdAt': 1569974399, 'proposer': None, 'trash': 'trash'},
            {'createdAt': 1577923200, 'proposer': None, 'trash': 'trash'},
        ])
        out: List[int] = []

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
