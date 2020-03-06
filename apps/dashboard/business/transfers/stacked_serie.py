"""
   Descp: Stacked serie transfer for multiple 'y' axis values.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List

from logs import LOGS
from apps.dashboard.business.transfers.serie import Serie

class StackedSerie():
    """
    * serie = see Serie
    * y_stack = each element of y_stack is a list of values on the serie.
    """

    def __init__(self, serie: Serie = None, y_stack: List[List] = None):

        self.serie = serie if serie else Serie()
        self.y_stack = y_stack if y_stack else list()


    def get_serie(self) -> List:
        if not self.serie:
            raise Exception(LOGS['attr_not_init']\
                .format('serie', 'get_serie'))

        return self.serie.get_x()


    def get_last_serie_elem(self) -> str:
        if not self.serie:
            raise Exception(LOGS['attr_not_init']\
                .format('serie', 'get_last_serie_elem'))

        return self.serie.get_last_serie_elem()


    def get_last_value(self, i_stack: int):
        return self.y_stack[i_stack][-1]

    
    def get_i_stack(self, i_stack: int) -> List:
        return self.y_stack[i_stack]
    

    def get_diff_last_values(self, i_stack: int) -> float:
        """
        A percentage of the diference among the last two values 
        on the 'i' stack.
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