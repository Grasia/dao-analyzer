"""
   Descp: Serie of values transfer.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
from pandas import Timestamp

from src.apps.daostack.resources.strings import TEXT

class Serie():
    """
    * x = a list of values which represent the serie.
    """

    def __init__(self, x: List = None):
        self.x: List = x if x else list()

    
    def get_last_serie_elem(self) -> str:
        val: str = TEXT['no_data']
        if self.x:
            val = f'{self.x[-1]}'

            if type(self.x[-1]) == Timestamp:
                val = self.x[-1].strftime('%B')
                
        return val 


    def get_x(self) -> List:
        return self.x