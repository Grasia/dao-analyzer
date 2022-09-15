"""
   Descp: This transfer has a stack of StackedSerie.
          Use it for example for multiple stacked bar chart.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List

from dao_analyzer.web.logs import LOGS
from dao_analyzer.web.apps.common.business.transfers.serie import Serie
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie

class NStackedSerie():
    """
    NStackedSerie uses StackedSerie and Serie with composition 
    instead of inheritance for better readability and traceability.

    * serie: see Serie.
    * sseries: a list of stacked 'y' axis sseries. See StackedSerie
    """

    def __init__(self, serie: Serie = None, sseries: List[StackedSerie] = None):
        self.__serie = serie if serie else Serie()
        self.__sseries = sseries if sseries else list()


    def get_serie(self) -> List:
        if not self.__serie:
            raise Exception(LOGS['attr_not_init']
                .format('serie', 'get_serie'))

        return self.__serie.get_x()

    
    def get_last_serie_elem(self) -> str:
        if not self.__serie:
            raise Exception(LOGS['attr_not_init']
                .format('serie', 'get_last_serie_elem'))

        return self.__serie.get_last_serie_elem()


    def get_last_value(self, i_value: int, j_stack: int) -> int:
        if not self.__sseries:
            raise Exception(LOGS['attr_not_init']
                .format('sseries', 'get_last_value'))

        return self.__sseries[i_value].get_last_value(j_stack)

    
    def get_i_stack(self, i_value: int, j_stack: int) -> List[int]:
        if not self.__sseries:
            raise Exception(LOGS['attr_not_init']
                .format('sseries', 'get_i_stack'))

        return self.__sseries[i_value].get_i_stack(j_stack)


    def get_diff_last_sseries(self, i_value: int, j_stack: int) -> int:
        if not self.__sseries:
            raise Exception(LOGS['attr_not_init']
                .format('sseries', 'get_diff_last_sseries'))

        return self.__sseries[i_value].get_diff_last_sseries(j_stack)


    def get_i_sserie(self, i: int) -> StackedSerie:
        if i >= len(self.__sseries):
            return StackedSerie()

        return self.__sseries[i]