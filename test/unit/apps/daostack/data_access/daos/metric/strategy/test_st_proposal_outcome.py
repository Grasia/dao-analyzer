"""
   Descp: Tester for StProposalOutcome.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd

from test.mocks.unix_date_builder import UnixDateBuilder
from dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.\
    st_proposal_outcome import StProposalOutcome
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.n_stacked_serie import NStackedSerie

class StProposalOutcomeTest(unittest.TestCase):

    def __get_in_data_success_ratio(self) -> pd.DataFrame:
        bl: UnixDateBuilder = UnixDateBuilder()
        boost_date: int = bl.sub(month=3).change(day=2, hour=0, minute=0, second=0).unix()

        return pd.DataFrame([
            #executedAt = today_year-(today_month-3)-25T10:00:00+00:00; boostedAt = today_year-(today_month-3)-02T00:00:00+00:00
            {'executedAt': bl.change(day=25, hour=10).unix(), 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'boostedAt': boost_date, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = today_year-(today_month-3)-02T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.change(day=2, hour=0).unix(), 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = today_year-(today_month-3)-20T00:00:00+00:00; boostedAt = today_year-(today_month-3)-02T00:00:00+00:00
            {'executedAt': bl.change(day=20).unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '0', 'boostedAt': boost_date, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = today_year-(today_month-2)-05T00:00:00+00:00; boostedAt = today_year-(today_month-3)-02T00:00:00+00:00
            {'executedAt': bl.add(month=1).change(day=5).unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '1', 'boostedAt': boost_date, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = today_year-(today_month-2)-05T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '1', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},

            #executedAt = today_year-(today_month-1)-28T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.add(month=1).change(day=28).unix(), 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '30', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = today_year-today_month-28T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.add(month=1).unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '0', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
        ])


    def test_process_data_boost_outcome(self):
        bl: UnixDateBuilder = UnixDateBuilder()
        bl_b: UnixDateBuilder = UnixDateBuilder()

        bl.sub(month=3).change(day=21, hour=10, minute=0, second=0)
        bl_b.sub(month=3).change(day=2, hour=0, minute=0, second=0)

        in_df: pd.DataFrame = pd.DataFrame([
            #executedAt = today_year-(today_month-3)-21T10:00:00+00:00; boostedAt = today_year-(today_month-3)-02T00:00:00+00:00
            {'executedAt': bl.unix(), 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'boostedAt': bl_b.unix(), 'queuedVoteRequiredPercentage': '50'},

            #executedAt = today_year-(today_month-3)-02T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.change(day=2, hour=0).unix(), 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '25', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = today_year-(today_month-1)-06T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.add(month=2).change(day=6).unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '2', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = today_year-(today_month-1)-28T00:00:00+00:00; boostedAt = today_year-(today_month-1)-06T00:00:00+00:00
            {'executedAt': bl.change(day=28).unix(), 'winningOutcome': 'Fail', 'totalRepWhenExecuted': '50', 'votesFor': '2', 'boostedAt': bl_b.add(month=2).change(day=6).unix(), 'queuedVoteRequiredPercentage': '50'},
            
            #executedAt = today_year-today_month-21T00:00:00+00:00; boostedAt = None
            {'executedAt': bl.add(month=1).change(day=21).unix(), 'winningOutcome': 'Pass', 'totalRepWhenExecuted': '50', 'votesFor': '0', 'boostedAt': None, 'queuedVoteRequiredPercentage': '50'},
        ])
        out: List[List[int]] = [
            [1, 0, 0, 0], # fn
            [1, 0, 0, 0], # tp
            [0, 0, 1, 0], # fp
            [0, 0, 1, 1], # tn
        ]

        strategy: StProposalOutcome = StProposalOutcome(m_type=0)
        result: StackedSerie = strategy.process_data(df=in_df)

        for i, l in enumerate(out, 0):
            res_list: List[int] = result.get_i_stack(i_stack=i)
            self.assertListEqual(l, res_list, f'stack = {i}')


    def test_process_data_total_success_ratio(self):
        in_df = self.__get_in_data_success_ratio()
        out: List[int] = [0.3333, 0.5, 0, 1.0]

        strategy: StProposalOutcome = StProposalOutcome(m_type=2)
        result: StackedSerie = strategy.process_data(df=in_df)

        self.assertListEqual(out, result.get_i_stack(0))


    def test_process_data_boost_success_ratio(self):
        in_df = self.__get_in_data_success_ratio()
        out: List[List[int]] = [
            [0.5, 0, None, None],
            [0.0, 1.0, 0, 1.0],
        ]

        strategy: StProposalOutcome = StProposalOutcome(m_type=1)
        result: NStackedSerie = strategy.process_data(df=in_df)

        for i, l in enumerate(out, 0):
            res_list: List[int] = result.get_i_stack(i_value=i, j_stack=0)
            self.assertListEqual(l, res_list, f'stack = {i}')


if __name__ == "__main__":
    unittest.main()
