"""
   Descp: Tester for StActiveUsers.

   Created on: 24-aug-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd
from datetime import datetime
from dateutil import relativedelta

from src.apps.daostack.data_access.daos.metric.strategy.\
    st_active_users import StActiveUsers
from src.apps.common.business.transfers.stacked_serie import StackedSerie


class StActiveUsersTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int]) -> None:
        strategy: StActiveUsers = StActiveUsers()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data1(self):
        in_df: pd.DataFrame = pd.DataFrame([
            {'createdAt': 1571961600, 'voter': '0', 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1571961600, 'proposer': '0', 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1572649200, 'staker': '0', 'trash': 'trash'}, #2019-11-01T23:00:00+00:00
            {'createdAt': 1569974399, 'voter': '1', 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1569974399, 'voter': '1', 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1576368000, 'proposer': '3', 'trash': 'trash'}, #2019-12-15T00:00:00+00:00
            {'createdAt': 1577750400, 'voter': '2', 'trash': 'trash'}, #2019-12-31T00:00:00+00:00
            {'createdAt': 1577750400, 'staker': '3', 'trash': 'trash'}, #2019-12-31T00:00:00+00:00
        ])
        delta = relativedelta.relativedelta(datetime.now(), datetime.fromtimestamp(1577750400))
        out: List[int] = [2, 1, 2] + [0] * (delta.months + 1)

        self.__check_lists(df=in_df, out=out)

        
    def test_process_data2(self):
        in_df: pd.DataFrame = pd.DataFrame([
            {'createdAt': 1571961600, 'staker': '0', 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1571961600, 'staker': '1', 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1572649200, 'staker': '1', 'trash': 'trash'}, #2019-11-01T23:00:00+00:00
            {'createdAt': 1569974399, 'staker': '2', 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1569974399, 'staker': '2', 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1577923200, 'staker': '3', 'trash': 'trash'}, #2020-01-02T00:00:00+00:00
        ])
        delta = relativedelta.relativedelta(datetime.now(), datetime.utcfromtimestamp(1577923200))
        out: List[int] = [3, 1, 0, 1] + [0] * (delta.months)

        self.__check_lists(df=in_df, out=out)


    def test_process_data3(self):
        in_df: pd.DataFrame = pd.DataFrame([
            {'createdAt': 1571961600, 'proposer': None, 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1571961600, 'proposer': None, 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1572649200, 'proposer': None, 'trash': 'trash'}, #2019-11-01T23:00:00+00:00
            {'createdAt': 1569974399, 'proposer': None, 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1569974399, 'proposer': None, 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1577923200, 'proposer': None, 'trash': 'trash'}, #2020-01-02T00:00:00+00:00
        ])
        
        out: List[int] = []

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
