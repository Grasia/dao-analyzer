"""
   Descp: Stacked time serie transfer for multiple y axis values.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from pandas import Timestamp

from logs import LOGS
from apps.dashboard.business.transfers.time_series import TimeSeries

class StackedTimeSerie():
    """
    * time_serie = see TimeSeries
    * y_stack = each element of y_stack is a list of values in a time serie.

    * month_over_month = a percentage of the amount among the last two months.
    """

    def __init__(self, time_serie: TimeSeries = None, 
    y_stack: List[List[int]] = None):

        self.time_serie = time_serie if time_serie else TimeSeries()
        self.y_stack = y_stack if y_stack else list(list())


    def get_time_serie(self) -> List[Timestamp]:
        if not self.time_serie:
            raise Exception(LOGS['attr_not_init']\
                .format('time_serie', 'get_time_serie'))

        return self.time_serie.get_x()


    def get_last_month(self) -> str:
        if not self.time_serie:
            raise Exception(LOGS['attr_not_init']\
                .format('time_serie', 'get_last_month'))

        return self.time_serie.get_last_month()


    def get_last_month_amount(self, i_stack: int) -> int:
        return self.y_stack[i_stack][-1]

    
    def get_y_stack(self, i_stack: int) -> List[int]:
        return self.y_stack[i_stack]
    

    def get_month_over_month(self, i_stack: int) -> float:
        """
        A percentage of the diference among the last two months.
        """
        y: List[int] = self.y_stack[i_stack]
        val = 0.0

        # indexes to access n-1 and n-2 positions in y[n] 
        i_1 = -1
        i_2 = -(2 % (len(y) + 1))

        divider: int = y[i_1] + y[i_2]

        if divider > 0:
            val = (y[i_1] - y[i_2]) / divider * 100

        return val