"""
   Descp: Votes type metric strategy test.

   Created on: 8-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.\
    st_votes_type import StVotesType

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StVotesTypeTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[List[int]]) -> None:
        strategy: StVotesType = StVotesType()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out[0], result.get_i_stack(i_stack=0)) # test negatives
        self.assertListEqual(out[1], result.get_i_stack(i_stack=1)) # test positives


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=1, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'uintVote': 1, 'createdAt': bl.unix()},#today_year-(today_month-3)-01T00:00:00+00:00
            {'uintVote': 1, 'createdAt': bl.add(month=1).change(day=25).unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'uintVote': 2, 'createdAt': bl.unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'uintVote': 2, 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()},#today_year-(today_month-1)-01T23:00:00+00:00
            {'uintVote': 1, 'createdAt': bl.sub(month=1).change(minute=59, second=59).unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'uintVote': 1, 'createdAt': bl.unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'uintVote': 1, 'createdAt': bl.add(month=2, second=1).change(day=21).unix()},#today_year-today_month-21T00:00:00+00:00
        ])

        out: List[List[int]] = [
            [0, 1, 1, 0], # number of votes against
            [1, 3, 0, 1]# number of votes for
        ]

        self.__check_lists(df=in_df, out=out)


    def test_process_data_votes_against(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=1, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'uintVote': 2, 'createdAt': bl.unix()},#today_year-(today_month-3)-01T00:00:00+00:00
            {'uintVote': 2, 'createdAt': bl.add(month=1).change(day=11).unix()},#today_year-(today_month-2)-11T00:00:00+00:00
            {'uintVote': 2, 'createdAt': bl.unix()},#today_year-(today_month-2)-11T00:00:00+00:00
            {'uintVote': 2, 'createdAt': bl.sub(month=1).change(day=3, hour=5).unix()},#today_year-(today_month-3)-03T5:00:00+00:00
            {'uintVote': 2, 'createdAt': bl.add(month=1).change(day=1, minute=59, second=59).unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'uintVote': 2, 'createdAt': bl.unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'uintVote': 2, 'createdAt': bl.change(day=21, hour=0, minute=0, second=0).unix()},#today_year-(today_month-2)-21T00:00:00+00:00
        ])

        out: List[List[int]] = [
            [2, 5, 0, 0], # number of votes against
            [0, 0, 0, 0]# number of votes for
        ]

        self.__check_lists(df=in_df, out=out)

if __name__ == "__main__":
    unittest.main()
