"""
   Descp: Organization transfers.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from pandas import Timestamp
from typing import List, Dict

from src.apps.daostack.resources.strings import TEXT


class Organization():
    def __init__(self, o_id: str = TEXT['no_data'], name: str = TEXT['no_data']):
        self.id: str = o_id
        self.name: str = name


class OrganizationList():
    __ALL_ORGS_ID: str = '1'


    def __init__(self, orgs: List[Organization] = None):
        self.__orgs: List[Organization] = orgs if orgs else list()


    def add_organization(self, org: Organization):
        if org:
            self.__orgs.append(org)


    def get_dict_representation(self):
        if not self.__orgs:
            return list()
        
        transformer = lambda x: {'value': x.id, 'label': x.name} 
        result: List[Dict[str, str]] = list(map(transformer, self.__orgs))
        result = sorted(result, key = lambda k: k['label'])
        # Add All Orgs selector
        all_orgs = {'value': self.__ALL_ORGS_ID, 'label': TEXT['all_orgs']}

        # Append it as the first one
        result = [all_orgs] + result
        return result


    def is_empty(self):
        return len(self.__orgs) == 0


    def get_ids_from_id(self, o_id: str) -> List[str]:
        """
        Gets a list of ids from a o_id attr.
        If o_id is equals to 'all orgs' id then returns a list with all the orgs id.
        If not returns a list with o_id as unique element of the list.
        """
        if self.is_empty():
            return list()

        if not o_id == self.__ALL_ORGS_ID:
            return [o_id]

        mapper = lambda x: x.id
        return list(map(mapper, self.__orgs))