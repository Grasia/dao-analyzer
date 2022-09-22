"""
   Descp: Stacked serie transfer for multiple 'y' axis values.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Tuple

from dao_analyzer.web.logs import LOGS
from dao_analyzer.web.apps.common.business.transfers.serie import Serie

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

    def get_last_values(self, i_stack: int = 0, add_stacks: bool = False) -> Tuple[float, float]:
        """
        Returns the last two values (this month and prev)
        to be able to calculate the difference between them

        * Returns this, prev
        """
        if add_stacks:
            i_stack = 0

        if i_stack >= len(self.y_stack):
            return 0.0, 0.0

        y: List = self.y_stack[i_stack]

        i_1 = -1
        i_2 = -(2 % (len(y) + 1))
        op1 = y[i_1]
        op2 = y[i_2]

        if op1 and op2 and add_stacks:
            for j in range(i_stack+1, len(self.y_stack)):
                y = self.y_stack[j]
                op1 += y[i_1]
                op2 += y[i_2]
        
        return op1, op2
    
    def get_diff_last_values(self, **kwargs) -> float:
        this, prev = self.get_last_values(**kwargs)

        if this is None:
            this = 0.0

        if prev is None:
            prev = 0.0
        
        return this - prev

    def get_rel_last_values(self, **kwargs)\
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
        this, prev = self.get_last_values(**kwargs)

        if this is None:
            this = 0.0

        if prev is None:
            prev = 0.0

        val: float = 0.0
        denominator = (this + prev)
        numerator = (this - prev)

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
