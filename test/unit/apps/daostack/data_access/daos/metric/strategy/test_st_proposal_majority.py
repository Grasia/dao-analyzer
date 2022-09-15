"""
   Descp: Test for StProposalMajority class

   Created on: 20-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
import numpy as np
import unittest
from typing import List

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_proposal_majority import StProposalMajority
from dao_analyzer.web.apps.common.business.transfers.n_stacked_serie import NStackedSerie    

class StProposalMajorityTest(unittest.TestCase):
    
    def test_process_data(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        boost_date: int = bl.sub(month=3).change(day=28, hour=0, minute=0, second=0).unix()

        in_df: pd.DataFrame = pd.DataFrame([
            #executedAt = today_year-(today_month-3)-25T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.change(day=25).unix(), 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'votesAgainst': '5', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = today_year-(today_month-3)-21T23:00:00+00:00; boostedAt = today_year-(today_month-2)-28T00:00:00+00:00
            {'executedAt': bl.change(day=21, hour=23).unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '5', 'votesAgainst': '30', 'boostedAt': boost_date, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = today_year-(today_month-2)-01T12:00:00+00:00; boostedAt = today_year-(today_month-2)-28T00:00:00+00:00
            {'executedAt': bl.add(month=1).change(day=1, hour=12).unix(), 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '5', 'votesAgainst': '1', 'boostedAt': boost_date, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = today_year-(today_month-2)-15T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.change(day=15, hour=0).unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '1', 'votesAgainst': '15', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = today_year-today_month-05T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.add(month=2).change(day=5).unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '0', 'votesAgainst': '0', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
        ])
        out: List[List[int]] = [
            [50.0, np.nan, np.nan, np.nan], #abs_passes
            [np.nan, 10.0, np.nan, np.nan], #rel_passes
            [np.nan, 30.0, np.nan, 0.0], #rel_fails
            [60.0, np.nan, np.nan, np.nan] #abs_fails
        ]

        strategy: StProposalMajority = StProposalMajority()
        result: NStackedSerie = strategy.process_data(df=in_df)

        # numpy takes into consideration nan values
        for i, l in enumerate(out, 0):
            res_list: List[int] = result.get_i_stack(i_value=i, j_stack=0)
            np.testing.assert_array_equal(l, res_list)


if __name__ == "__main__":
    unittest.main()
