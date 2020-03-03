"""
   Descp: Stacked time series transfer.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from pandas import Timestamp

from apps.dashboard.business.transfers.metric_time_series import MetricTimeSeries

class MetricStackTimeSeries():
    """
    """

    def __init__(self, x: List[Timestamp] = None, y1: List[int] = None, \
        y2: List[int] = None, m_type: int = MetricTimeSeries.METRIC_TYPE_NO_TYPE):

        self.basic_time_serie = MetricTimeSeries(x=x, y=y1, m_type=m_type)
        self.y2 = y2 if y2 else list()