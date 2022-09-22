"""
   Descp: Vote outcome metric strategy test.

   Created on: 21-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.aragon.data_access.daos.metric.strategy.\
    st_vote_outcome import StVoteOutcome

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StVoteOutcomeTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[List[int]]) -> None:
        strategy: StVoteOutcome = StVoteOutcome()
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out[0], result.get_i_stack(i_stack=0)) # test rejections
        self.assertListEqual(out[1], result.get_i_stack(i_stack=1)) # test passes


    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl.sub(month=3).change(day=16, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            {'yea': 0, 'nay': 1, 'supportRequiredPct': 15, 'minAcceptQuorum': 100000000000000000, 'votingPower': 5,'startDate': bl.unix()},#today_year-(today_month-3)-16T00:00:00+00:00
            {'yea': 6, 'nay': 2, 'supportRequiredPct': 50, 'minAcceptQuorum': 50, 'votingPower': 9,'startDate': bl.add(month=1).change(day=5).unix()},#today_year-(today_month-2)-05T00:00:00+00:00
            {'yea': 1, 'nay': 0, 'supportRequiredPct': 100000000000000000, 'minAcceptQuorum': 330000000000000000, 'votingPower': 3,'startDate': bl.unix()},#today_year-(today_month-2)-05T00:00:00+00:00
            {'yea': 5, 'nay': 4, 'supportRequiredPct': 330000000000000000, 'minAcceptQuorum': 150000000000000000, 'votingPower': 9,'startDate': bl.add(month=2).change(day=1, hour=23, minute=59, second=59).unix()},#today_year-today_month-01T23:59:59+00:00
            {'yea': 0, 'nay': 0, 'supportRequiredPct': 0, 'minAcceptQuorum': 1, 'votingPower': 00000000000000000,'startDate': bl.unix()},#today_year-today_month-01T23:59:59+00:00
            {'yea': 4, 'nay': 0, 'supportRequiredPct': 1000000000000000000, 'minAcceptQuorum': 500000000000000000, 'votingPower': 10,'startDate': bl.add(second=1).change(day=27).unix()},#today_year-today_month-27T00:00:00+00:00
        ])
        out: List[List[int]] = [
            [1, 0, 0, 2], # number of rejected proposals
            [0, 2, 0, 1] # number of approved proposals
        ]

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
