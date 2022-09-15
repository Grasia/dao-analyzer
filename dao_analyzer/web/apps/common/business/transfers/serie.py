"""
   Descp: Serie of values transfer.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from datetime import date

from dao_analyzer.web.apps.common.resources.strings import TEXT

class Serie():
    """
    * __x = a list of values which represent the serie.
    """

    def __init__(self, x: List = None):
        self.__x: List = x if x else list()

    
    def get_last_serie_elem(self) -> str:
        if not self.__x:
            return TEXT['no_data']

        val = f'{self.__x[-1]}'

        if type(self.__x[-1]) == date:
            val = self.__x[-1].strftime('%B')
                
        return val 


    def get_x(self) -> List:
        return self.__x
