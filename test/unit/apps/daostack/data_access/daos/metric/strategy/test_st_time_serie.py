"""
   Descp: Tester for StTimeSerie.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from typing import List
import pandas as pd
from dateutil import relativedelta
from datetime import datetime

from src.apps.daostack.data_access.daos.metric.strategy.\
    st_time_serie import StTimeSerie

from src.apps.common.business.transfers.stacked_serie import StackedSerie


class StTimeSerieTest(unittest.TestCase):

    def __check_lists(self, df: pd.DataFrame, out: List[int]) -> None:
        # m_type it not used, in the future -1 will break it
        strategy: StTimeSerie = StTimeSerie(m_type=-1)
        result: StackedSerie = strategy.process_data(df=df)

        self.assertListEqual(out, result.get_i_stack(i_stack=0))


    def test_process_data(self):
        in_df: pd.DataFrame = pd.DataFrame([
            {'createdAt': 1567296000, 'id': '-1', 'trash': 'trash'}, #2019-09-01T00:00:00+00:00
            {'createdAt': 1571961600, 'id': '3', 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1571961600, 'id': '0', 'trash': 'trash'}, #2019-10-25T00:00:00+00:00
            {'createdAt': 1572649200, 'id': '0', 'trash': 'trash'}, #2019-11-01T23:00:00+00:00
            {'createdAt': 1569974399, 'id': '1', 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1569974399, 'id': '1', 'trash': 'trash'}, #2019-10-01T23:59:59+00:00
            {'createdAt': 1577750400, 'id': '2', 'trash': 'trash'}, #2019-12-31T00:00:00+00:00
        ])
        delta = relativedelta.relativedelta(datetime.now(), datetime.fromtimestamp(1577750400))
        out: List[int] = [1, 4, 1, 1] + [0] * (delta.months + 1)

        self.__check_lists(df=in_df, out=out)


if __name__ == "__main__":
    unittest.main()
