"""
   Descp: A class to warp a query abstraction.

   Created on: 26-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import Dict

class Query():
    """
    Atrrs:
        * body: a list of params or a Query object if you want neasted queries.
        * filters: a list of filter in a dictionary.
    """
    
    def __init__(self, header: str = '', body = None, 
    filters: Dict[str, str] = None):

        self.header = header
        # body could be a List[str] or Query 
        self.body = body if body else list()
        self.filters: Dict[str, str] = filters if filters else dict()