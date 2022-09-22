"""
   Descp: Proposal type metric strategy test.

   Created on: 9-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.\
    st_proposal_type import StProposalType

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StProposalTypeTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[List[int]]) -> None:
        strategy: StProposalType = StProposalType()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out[0], result.get_i_stack(i_stack=0)) # test others
        self.assertListEqual(out[1], result.get_i_stack(i_stack=1)) # test donations
        self.assertListEqual(out[2], result.get_i_stack(i_stack=2)) # test new members
        self.assertListEqual(out[3], result.get_i_stack(i_stack=3)) # test grants


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=1, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'sharesRequested': 0, 'tributeOffered': 0, 'createdAt': bl.unix()},#today_year-(today_month-3)-01T00:00:00+00:00
            {'sharesRequested': 2, 'tributeOffered': 0, 'createdAt': bl.change(day=25).unix()},#today_year-(today_month-3)-25T00:00:00+00:00
            {'sharesRequested': 0, 'tributeOffered': 100, 'createdAt': bl.unix()},#today_year-(today_month-3)-25T00:00:00+00:00
            {'sharesRequested': 1, 'tributeOffered': 0, 'createdAt': bl.add(month=1).unix()},#today_year-(today_month-2)-25T00:00:00+00:00
            {'sharesRequested': 55, 'tributeOffered': 0, 'createdAt': bl.change(day=1, hour=23).unix()},#today_year-(today_month-2)-01T23:00:00+00:00
            {'sharesRequested': 0, 'tributeOffered': -1, 'createdAt': bl.change(minute=59, second=59).unix()},#today_year-(today_month-2)-01T23:59:59+00:00
            {'sharesRequested': -1, 'tributeOffered': -2, 'createdAt': bl.add(month=1).unix()},#today_year-(today_month-1)-01T23:59:59+00:00
            {'sharesRequested': 0, 'tributeOffered': 1, 'createdAt': bl.add(second=1).change(day=18).unix()},#today_year-(today_month-1)-18T00:00:00+00:00
            {'sharesRequested': 99, 'tributeOffered': 22, 'createdAt': bl.add(month=1).change(day=21).unix()},#today_year-today_month-21T00:00:00+00:00
        ])
        out: List[List[int]] = [
            [1, 1, 1, 0], # other proposals
            [1, 0, 1, 0], # donation proposals
            [0, 0, 0, 1], # new member proposals
            [1, 2, 0, 0], # grant proposals
        ]

        self.__check_lists(df=in_df, out=out)


    def test_process_data_others(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=2).change(day=17, hour=6, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'sharesRequested': 0, 'tributeOffered': 0, 'createdAt': bl.unix()},#today_year-(today_month-2)-17T00:06:00+00:00
            {'sharesRequested': 0, 'tributeOffered': -5, 'createdAt': bl.add(month=1).change(day=18, hour=18).unix()},#today_year-(today_month-1)-18T18:00:00+00:00
            {'sharesRequested': -5, 'tributeOffered': 0, 'createdAt': bl.add(month=1).change(day=28, minute=18).unix()},#today_year-today_month-28T18:18:00+00:00
        ])
        out: List[List[int]] = [
            [1, 1, 1], # other proposals
            [0, 0, 0], # donation proposals
            [0, 0, 0], # new member proposals
            [0, 0, 0], # grant proposals
        ]

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
