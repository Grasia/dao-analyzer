"""
   Descp: Installed apps test.

   Created on: 20-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List, Dict
import pandas as pd

from dao_analyzer.web.apps.aragon.data_access.daos.metric.strategy.\
    st_installed_apps import StInstalledApps

from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie


class StInstalledAppsTest(unittest.TestCase):

    def test_repeated_names(self):

        in_df: pd.DataFrame = pd.DataFrame([
            {'trash': 'trash', 'id': '1', 'repoName': '1'},
            {'trash': 'trash', 'id': '2', 'repoName': '2'},
            {'trash': 'trash', 'id': '3', 'repoName': '3'},
            {'trash': 'trash', 'id': '4', 'repoName': '1'},
        ])
        strategy: StInstalledApps = StInstalledApps()
        result: StackedSerie = strategy.process_data(df=in_df)
        out: List[int] = [2, 1, 1]

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_repeated_non_names(self):

        in_df: pd.DataFrame = pd.DataFrame([
            {'trash': 'trash', 'id': '1', 'repoName': '1'},
            {'trash': 'trash', 'id': '2', 'repoName': '2'},
            {'trash': 'trash', 'id': '3', 'repoName': None},
            {'trash': 'trash', 'id': '4', 'repoName': None},
        ])
        strategy: StInstalledApps = StInstalledApps()
        result: StackedSerie = strategy.process_data(df=in_df)
        out: List[int] = [1, 1]

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_repetitions(self):

        in_df: pd.DataFrame = pd.DataFrame([
            {'trash': 'trash', 'id': '1', 'repoName': '1'},
            {'trash': 'trash', 'id': '1', 'repoName': '1'},
            {'trash': 'trash', 'id': '1', 'repoName': '1'},
        ])
        strategy: StInstalledApps = StInstalledApps()
        result: StackedSerie = strategy.process_data(df=in_df)
        out: List[int] = [1]

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_others(self):
        max_elems: int = 15

        in_data: List[Dict[str, str]] = [
            {'id': '1', 'repoName': '1'},
            {'id': '2', 'repoName': '1'},
            {'id': '3', 'repoName': '1'},
        ] + \
        [{'id': f'{i}', 'repoName': f'{i}'} for i in range(4, max_elems+6)]

        in_df: pd.DataFrame = pd.DataFrame(in_data)
        strategy: StInstalledApps = StInstalledApps()
        result: StackedSerie = strategy.process_data(df=in_df)

        out: List[int] = [3] + ([1] * (max_elems-1)) + [3] 

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


if __name__ == "__main__":
    unittest.main()
