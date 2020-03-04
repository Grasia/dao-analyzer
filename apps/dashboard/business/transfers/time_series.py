"""
   Descp: Time series transfer.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from pandas import Timestamp

from apps.dashboard.resources.strings import TEXT

class TimeSeries():
    """
    * x = a list with timestamps month over month.
    """

    def __init__(self, x: List[Timestamp] = None):
        self.x: List[Timestamp] = x if x else list()

    
    def get_last_month(self) -> str:
        return self.x[-1].strftime('%B') if self.x else TEXT['no_data']


    def get_x(self) -> List[Timestamp]:
        return self.x