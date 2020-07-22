"""
   Descp: Tester for StProposalOutcome.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List, Tuple
import pandas as pd
from dateutil import relativedelta
from datetime import datetime

from src.apps.daostack.data_access.daos.metric.strategy.\
    st_proposal_outcome import StProposalOutcome

from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.n_stacked_serie import NStackedSerie

class StProposalOutcomeTest(unittest.TestCase):

    def __get_out(self, num_months: int, 
        tp: List[int], tn: List[int], fp: List[int], fn: List[int]) -> List[List[int]]:

        prev: List[List[int]] = [fn, tp, fp, tn]
        out: List[List[int]] = list()
        for vals in prev:
            vals += [0] * num_months
            out.append(vals)

        return out


    def __get_in_data_success_ratio(self) -> Tuple[pd.DataFrame, int]:
        return (pd.DataFrame([
            #executedAt = 2019-12-31T10:00:00+00:00; boostedAt = 2019-12-02T00:00:00+00:00
            {'executedAt': 1577786400, 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'boostedAt': 1575244800, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = 2019-12-02T00:00:00+00:00; boostedAt = None
            {'executedAt': 1575244800, 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = 2019-12-20T00:00:00+00:00; boostedAt = 2019-12-02T00:00:00+00:00
            {'executedAt': 1576800000, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '0', 'boostedAt': 1575244800, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = 2020-01-05T00:00:00+00:00; boostedAt = 2019-12-02T00:00:00+00:00
            {'executedAt': 1578182400, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '1', 'boostedAt': 1575244800, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = 2020-01-05T00:00:00+00:00; boostedAt = None
            {'executedAt': 1578182400, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '1', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = 2020-02-28T00:00:00+00:00; boostedAt = None
            {'executedAt': 1582848000, 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '30', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = 2020-03-31T00:00:00+00:00; boostedAt = None
            {'executedAt': 1585612800, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '0', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
        ]),
        1585612800)


    def test_process_data_boost_outcome(self):
        in_df: pd.DataFrame = pd.DataFrame([
            #executedAt = 2019-12-31T10:00:00+00:00; boostedAt = 2019-12-02T00:00:00+00:00
            {'executedAt': 1577786400, 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'boostedAt': 1575244800, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = 2019-12-02T00:00:00+00:00; boostedAt = None
            {'executedAt': 1575244800, 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = 2020-02-06T00:00:00+00:00; boostedAt = None
            {'executedAt': 1580947200, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '2', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = 2020-02-28T00:00:00+00:00; boostedAt = 2020-02-06T00:00:00+00:00
            {'executedAt': 1582848000, 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '2', 'boostedAt': 1580947200, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = 2020-03-31T00:00:00+00:00; boostedAt = None
            {'executedAt': 1585612800, 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '0', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
        ])
        delta = relativedelta.relativedelta(datetime.now(), datetime.fromtimestamp(1585612800))
        out: List[List[int]] = self.__get_out(
            num_months=delta.months+1,
            tp=[1, 0, 0, 0],
            tn=[0, 0, 1, 1],
            fp=[0, 0, 1, 0],
            fn=[1, 0, 0, 0])

        strategy: StProposalOutcome = StProposalOutcome(m_type=0)
        result: StackedSerie = strategy.process_data(df=in_df)

        for i, l in enumerate(out, 0):
            res_list: List[int] = result.get_i_stack(i_stack=i)
            self.assertListEqual(l, res_list, f'stack = {i}')


    def test_process_data_total_success_ratio(self):
        in_df, last_date = self.__get_in_data_success_ratio()
        delta = relativedelta.relativedelta(datetime.now(), datetime.fromtimestamp(last_date))
        out: List[int] = [0.3333, 0.5, 0, 1.0] + [None] * (delta.months+1)

        strategy: StProposalOutcome = StProposalOutcome(m_type=2)
        result: StackedSerie = strategy.process_data(df=in_df)

        self.assertListEqual(out, result.get_i_stack(0))


    def test_process_data_boost_success_ratio(self):
        in_df, last_date = self.__get_in_data_success_ratio()
        delta = relativedelta.relativedelta(datetime.now(), datetime.fromtimestamp(last_date))
        out: List[List[int]] = [
            [0.5, 0, None, None] + [None] * (delta.months+1),
            [0.0, 1.0, 0, 1.0] + [None] * (delta.months+1),
        ]

        strategy: StProposalOutcome = StProposalOutcome(m_type=1)
        result: NStackedSerie = strategy.process_data(df=in_df)

        for i, l in enumerate(out, 0):
            res_list: List[int] = result.get_i_stack(i_value=i, j_stack=0)
            self.assertListEqual(l, res_list, f'stack = {i}')


if __name__ == "__main__":
    unittest.main()
