"""
   Descp: Basic time series transfer.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from pandas import Timestamp
from apps.dashboard.presentation.strings import TEXT

class MetricTimeSeries():
    """
    * x = a list with timestamps month over month.
    * y = a list with n elems in a 'x' month.
    * last_month_amount = the amount in the last month.
    * last_month_name = last month's name.
    * month_over_month = a percentage of the amount among the last two months.
    * m_type = no type assigned, new users, new proposal
    """
    METRIC_TYPE_NO_TYPE: int = 0
    METRIC_TYPE_NEW_USERS: int = 1
    METRIC_TYPE_NEW_PROPOSAL: int = 2

    def __init__(self, x: List[Timestamp] = None, y: List[int] = None, 
        m_type: int = METRIC_TYPE_NO_TYPE):

        self.x: List[Timestamp] = x if x else list()
        self.y: List[int] = y if y else list()
        self.m_type = m_type
        self.last_month_amount: int = y[-1] if y else 0
        self.last_month_name: str = x[-1].strftime('%B') if x \
            else TEXT['no_data']

        self.month_over_month: float = self.__calculate_m_o_m() if y \
            else 0.0


    def __calculate_m_o_m(self) -> float:
        val = 0.0
        # indexes to access n-1 and n-2 positions in y[n] 
        i_1 = -1
        i_2 = -(2 % (len(self.y) + 1))

        divider: int = self.y[i_1] + self.y[i_2]
        if divider > 0:
            val = (self.y[i_1] - self.y[i_2]) / divider * 100

        return val