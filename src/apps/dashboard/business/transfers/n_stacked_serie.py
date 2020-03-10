"""
   Descp: This transfer has a stack of StackedSerie.
          Use it for example for multiple stacked bar chart.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List

from src.logs import LOGS
from src.apps.dashboard.business.transfers.serie import Serie
from src.apps.dashboard.business.transfers.stacked_serie import StackedSerie

class NStackedSerie():
    """
    NStackedSerie uses StackedSerie and Serie with composition 
    instead of inheritance for better readability and traceability.

    * serie: see Serie.
    * values: a list of stacked 'y' axis values. See StackedSerie
    """

    def __init__(self, serie: Serie = None, values: List[StackedSerie] = None):
        self.serie = serie if serie else Serie()
        self.values = values if values else list()


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


    def get_last_value(self, i_value: int, j_stack: int) -> int:
        if not self.values:
            raise Exception(LOGS['attr_not_init']
                .format('values', 'get_last_value'))

        return self.values[i_value].get_last_value(j_stack)

    
    def get_i_stack(self, i_value: int, j_stack: int) -> List[int]:
        if not self.values:
            raise Exception(LOGS['attr_not_init']
                .format('values', 'get_i_stack'))

        return self.values[i_value].get_i_stack(j_stack)


    def get_diff_last_values(self, i_value: int, j_stack: int) -> int:
        if not self.values:
            raise Exception(LOGS['attr_not_init']
                .format('values', 'get_diff_last_values'))

        return self.values[i_value].get_diff_last_values(j_stack)