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
from datetime import datetime
from dateutil import relativedelta

from src.apps.daostack.data_access.daos.metric.strategy.\
    st_proposal_majority import StProposalMajority
from src.apps.common.business.transfers.n_stacked_serie import NStackedSerie    

class StProposalMajorityTest(unittest.TestCase):

    def __get_out(self, num_months: int, 
        abs_passes: List[int], rel_passes: List[int], rel_fails: List[int],
        abs_fails: List[int]) -> List[List[int]]:

        prev: List[List[int]] = [abs_passes, rel_passes, rel_fails, abs_fails]
        out: List[List[int]] = list()
        for vals in prev:
            vals += [np.nan] * num_months
            out.append(vals)

        return out

    
    def test_process_data1(self):
        in_df: pd.DataFrame = pd.DataFrame([
            #executedAt = 2019-10-25T00:00:00+00:00; boostedAt = None
            {'executedAt': 1571961600, 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'votesAgainst': '5', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = 2019-10-31T23:00:00+00:00; boostedAt = 2019-10-30T00:00:00+00:00
            {'executedAt': 1572562800, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '5', 'votesAgainst': '30', 'boostedAt': 1572393600, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = 2019-11-01T12:00:00+00:00; boostedAt = 2019-10-30T00:00:00+00:00
            {'executedAt': 1572609600, 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '5', 'votesAgainst': '1', 'boostedAt': 1572393600, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = 2019-11-15T00:00:00+00:00; boostedAt = None
            {'executedAt': 1573776000, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '1', 'votesAgainst': '15', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = 2020-01-05T00:00:00+00:00; boostedAt = None
            {'executedAt': 1578182400, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '0', 'votesAgainst': '0', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
        ])
        delta = relativedelta.relativedelta(datetime.now(), datetime.utcfromtimestamp(1578182400))
        out: List[List[int]] = self.__get_out(
            num_months=(delta.months + 1), 
            abs_passes=[50.0, np.nan, np.nan, np.nan],
            rel_passes=[np.nan, 10.0, np.nan, np.nan],
            rel_fails=[np.nan, 30.0, np.nan, 0.0],
            abs_fails=[60.0, np.nan, np.nan, np.nan])

        strategy: StProposalMajority = StProposalMajority()
        result: NStackedSerie = strategy.process_data(df=in_df)

        # numpy takes into consideration nan values
        for i, l in enumerate(out, 0):
            res_list: List[int] = result.get_i_stack(i_value=i, j_stack=0)
            np.testing.assert_array_equal(l, res_list)


if __name__ == "__main__":
    unittest.main()
