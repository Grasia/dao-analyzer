"""
   Descp: Proposal outcome metric strategy test.

   Created on: 9-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.\
    st_proposal_outcome import StProposalOutcome

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StProposalOutcomeTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[List[int]]) -> None:
        strategy: StProposalOutcome = StProposalOutcome()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out[0], result.get_i_stack(i_stack=0)) # test rejections
        self.assertListEqual(out[1], result.get_i_stack(i_stack=1)) # test passes


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=16, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'didPass': False, 'processed': True, 'createdAt': bl.unix()},#today_year-(today_month-3)-16T00:00:00+00:00
            {'didPass': True, 'processed': True, 'createdAt': bl.add(month=1).change(day=5).unix()},#today_year-(today_month-2)-05T00:00:00+00:00
            {'didPass': False, 'processed': False, 'createdAt': bl.sub(month=1).unix()},#today_year-(today_month-3)-05T00:00:00+00:00
            {'didPass': True, 'processed': False, 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()},#today_year-(today_month-2)-01T23:00:00+00:00
            {'didPass': False, 'processed': True, 'createdAt': bl.add(month=2).change(minute=59, second=59).unix()},#today_year-today_month-01T23:59:59+00:00
            {'didPass': True, 'processed': True, 'createdAt': bl.unix()},#today_year-today_month-01T23:59:59+00:00
            {'didPass': True, 'processed': True, 'createdAt': bl.sub(month=2).add(second=1).change(day=27).unix()},#today_year-(today_month-2)-27T00:00:00+00:00
        ])
        out: List[List[int]] = [
            [1, 0, 0, 1], # number of rejected proposals
            [0, 2, 0, 1] # number of approved proposals
        ]

        self.__check_lists(df=in_df, out=out)


    def test_process_data_not_processed(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=16, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'didPass': True, 'processed': True, 'createdAt': bl.unix()},#today_year-(today_month-3)-16T00:00:00+00:00
            {'didPass': True, 'processed': False, 'createdAt': bl.add(month=1).change(day=5).unix()},#today_year-(today_month-2)-05T00:00:00+00:00
            {'didPass': False, 'processed': False, 'createdAt': bl.sub(month=1).unix()},#today_year-(today_month-3)-05T00:00:00+00:00
            {'didPass': True, 'processed': False, 'createdAt': bl.add(month=1).change(day=1, hour=23).unix()},#today_year-(today_month-2)-01T23:00:00+00:00
            {'didPass': False, 'processed': False, 'createdAt': bl.add(month=2).change(minute=59, second=59).unix()},#today_year-today_month-01T23:59:59+00:00
            {'didPass': True, 'processed': False, 'createdAt': bl.unix()},#today_year-today_month-01T23:59:59+00:00
            {'didPass': True, 'processed': False, 'createdAt': bl.sub(month=2).add(second=1).change(day=27).unix()},#today_year-(today_month-2)-27T00:00:00+00:00
        ])
        out: List[List[int]] = [
            [0, 0, 0, 0], # number of rejected proposals
            [1, 0, 0, 0] # number of approved proposals
        ]

        self.__check_lists(df=in_df, out=out)

if __name__ == "__main__":
    unittest.main()
