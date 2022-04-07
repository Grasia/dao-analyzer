"""
   Descp: Stacked serie transfer for multiple 'y' axis values.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List

from dao_analyzer.logs import LOGS
from dao_analyzer.apps.common.business.transfers.serie import Serie

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
            raise Exception(LOGS['attr_not_init']
                .format('serie', 'get_serie'))

        return self.serie.get_x()


    def get_last_serie_elem(self) -> str:
        if not self.serie:
            raise Exception(LOGS['attr_not_init']
                .format('serie', 'get_last_serie_elem'))

        return self.serie.get_last_serie_elem()


    def get_last_value(self, i_stack: int):
        if i_stack >= len(self.y_stack):
            return 0 
        return self.y_stack[i_stack][-1]

    
    def get_i_stack(self, i_stack: int) -> List:
        if i_stack >= len(self.y_stack):
            return list() 
        return self.y_stack[i_stack]
    

    def get_diff_last_values(self, i_stack: int = 0, add_stacks: bool = False)\
    -> float:
        """
        A percentage of the diference among the last two values.
        Parameters: 
            * i_stack: indicates the stack to operate. Default 0.
            * add_stacks: indicates whether you wish to operate over all
                          the stacks, if you enable this flag, i_stack don't
                          care. Default False.
        Return:
            A float. 
        """
        if add_stacks:
            i_stack = 0
        
        if i_stack >= len(self.y_stack):
            return 0.0

        y: List = self.y_stack[i_stack]
        val: float = 0.0

        # indexes to access n-1 and n-2 positions in y[n]
        i_1 = -1
        i_2 = -(2 % (len(y) + 1))
        op1 = y[i_1]
        op2 = y[i_2]

        if not op1 or not op2:
            return 0

        if add_stacks:
            for j in range(i_stack+1, len(self.y_stack)):
                y = self.y_stack[j]
                op1 += y[i_1]
                op2 += y[i_2]

        denominator = (op1 + op2)
        numerator = (op1 - op2)

        if denominator > 0:
            val = numerator / denominator * 100

        return val


    def get_n_stacks(self, n_stacks: int) -> List[List]:
        stacks: List[List] = list()

        for s in self.y_stack:
            stacks.append(s)
        # fill with the remainder n_stacks
        for _ in range(len(stacks), n_stacks):
            stacks.append(list())

        return stacks


    def get_stacks(self) -> List[List]:
        return self.y_stack
