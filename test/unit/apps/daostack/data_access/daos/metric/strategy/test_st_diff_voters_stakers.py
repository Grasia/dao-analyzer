"""
   Descp: Tester for StDifferentVS.

   Created on: 17-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_different_voters_stakers import StDifferentVS
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StDifferentVSTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int], stype: int) -> None:
        strategy: StDifferentVS = StDifferentVS(m_type=stype)
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data_voters(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'voter': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'voter': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-25T00:00:00+00:00
            {'voter': '0', 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-1)-01T23:00:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.sub(month=1).change(second=59, minute=59).unix()}, #today_year-(today_month-2)-01T23:59:00+00:00
            {'voter': '1', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-2)-01T23:59:59+00:00
            {'voter': '2', 'trash': 'trash', 'createdAt': bl.add(month=2).change(day=21, hour=0).unix()}, #today_year-today_month-21T00:59:00+00:00
        ])
        out: List[int] = [2, 1, 1]

        self.__check_lists(df=in_df, out=out, stype=0)

        
    def test_process_data_stakers(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=25, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'staker': '0', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-3)-25T00:00:00+00:00
            {'staker': '1', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-3)-25T00:00:00+00:00
            {'staker': '1', 'trash': 'trash', 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()}, #today_year-(today_month-2)-01T23:00:00+00:00
            {'staker': '2', 'trash': 'trash', 'createdAt': bl.sub(month=1).change(second=59, minute=59).unix()}, #today_year-(today_month-3)-01T23:59:00+00:00
            {'staker': '2', 'trash': 'trash', 'createdAt': bl.unix()}, #today_year-(today_month-3)-01T23:59:59+00:00
            {'staker': '3', 'trash': 'trash', 'createdAt': bl.add(month=3).change(day=2, hour=0).unix()}, #today_year-today_month-2T00:59:00+00:00
        ])
        out: List[int] = [3, 1, 0, 1]

        self.__check_lists(df=in_df, out=out, stype=1)


if __name__ == "__main__":
    unittest.main()
