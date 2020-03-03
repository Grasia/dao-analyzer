"""
   Descp: Organization transfers.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from pandas import Timestamp
from apps.dashboard.presentation.strings import TEXT

class Organization():
    def __init__(self, o_id:str = TEXT['no_data'], name:str = TEXT['no_data']):
        self.id: str   = o_id
        self.name: str = name 


class OrganizationUser():
    def __init__(self, created_at: Timestamp = None):
        self.created_at: Timestamp = created_at if created_at else Timestamp(0)