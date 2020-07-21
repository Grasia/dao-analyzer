"""
   Descp: Tester for StDifferentVS.

   Created on: 17-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd
from datetime import datetime
from dateutil import relativedelta

from src.apps.daostack.data_access.daos.metric.strategy.\
    st_different_voters_stakers import StDifferentVS
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie


class StDifferentVSTest(unittest.TestCase):

    def test_process_data1(self):
        in_df: pd.DataFrame = pd.DataFrame([
            {'createdAt': 1571961600, 'voter': '0', 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1571961600, 'voter': '0', 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1572649200, 'voter': '0', 'trash': 'trash'}, #2019-11-01T23:00:00+00:00
            {'createdAt': 1569974399, 'voter': '1', 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1569974399, 'voter': '1', 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1577836799, 'voter': '2', 'trash': 'trash'}, #2019-12-31T23:59:59+00:00
        ])
        delta = relativedelta.relativedelta(datetime.now(), datetime.utcfromtimestamp(1577836799))
        out: List[int] = [2, 1, 1] + [0] * (delta.months + 1)

        strategy: StDifferentVS = StDifferentVS(m_type=0)
        result: StackedSerie = strategy.process_data(df=in_df)
        for i, r in enumerate(result.get_i_stack(i_stack=0), 0):
            self.assertEqual(out[i], r)

        
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
        out: List[int] = [3, 1, 0, 1] + [0] * (delta.months + 1)

        strategy: StDifferentVS = StDifferentVS(m_type=1)
        result: StackedSerie = strategy.process_data(df=in_df)
        for i, r in enumerate(result.get_i_stack(i_stack=0), 0):
            self.assertEqual(out[i], r)


if __name__ == "__main__":
    unittest.main()
