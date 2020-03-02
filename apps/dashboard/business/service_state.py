"""
   Descp: Classes to save the app's state

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List

class ServiceState():
    """
    This class is used to save the app's state
    """
    ALL_ORGS_ID: str = '1'

    def __init__(self):
        self.organization_ids = list()

    
    def set_orgs_ids(self, ids: List[str]):
        self.organization_ids = ids