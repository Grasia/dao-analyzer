"""
   Descp: A class to warp a query abstraction.

   Created on: 26-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import Dict, List

class Query():
    """
    Atrrs:
        * body: a list of params or a Query object if you want neasted queries.
        * filters: a list of filter in a dictionary.
    
    TODO: neasted queries
    """
    
    def __init__(self, header: str, body: List[str], filters: Dict[str, str]):

        self.header = header
        self.body: Query = body
        self.filters: Dict[str, str] = filters