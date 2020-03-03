"""
   Descp: This transfer has a stack of StackedTimeSerie.
    Use it for example for multiple stacked bar chart.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from pandas import Timestamp

from logs import LOGS
from apps.dashboard.business.transfers.time_series import TimeSeries
from apps.dashboard.business.transfers.stacked_time_serie \
    import StackedTimeSerie

class NStackedTimeSerie():
    """
    NStackedTimeSerie uses StackedTimeSerie and TimeSeries with composition 
    instead of inheritance for better readability and traceability.

    * time_serie: see TimeSeries.
    * values: a list of stacked y axis values. See StackedTimeSerie
    """

    def __init__(self, time_serie: TimeSeries = None, 
        values: List[StackedTimeSerie] = None):

        self.time_serie = time_serie if time_serie else TimeSeries()
        self.values = values if values else list()


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

    
    def get_y_stack(self, i_value: int, j_stack: int) -> List[int]:
        if not self.values:
            raise Exception(LOGS['attr_not_init']\
                .format('values', 'get_y_stack'))

        return self.values[i_value].get_y_stack(j_stack)


    def get_last_month_amount(self, i_value: int, j_stack: int) -> int:
        if not self.values:
            raise Exception(LOGS['attr_not_init']\
                .format('values', 'get_last_month_amount'))

        return self.values[i_value].get_last_month_amount(j_stack)


    def get_month_over_month(self, i_value: int, j_stack: int) -> int:
        if not self.values:
            raise Exception(LOGS['attr_not_init']\
                .format('values', 'get_month_over_month'))

        return self.values[i_value].get_month_over_month(j_stack)
        