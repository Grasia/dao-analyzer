"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 17-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import Dict
import pandas as pd

from src.apps.daostack.business.transfers.organization import Organization
from src.apps.daostack.business.transfers.organization import OrganizationList
import src.apps.daostack.data_access.requesters.cache_requester as cache 


class DaoOrganizationList:
    def __init__(self, requester: cache.CacheRequester):
        self.__requester = requester


    def get_organizations(self) -> OrganizationList:
        df: pd.DataFrame = self.__requester.request(cache.DAOS)
        orgs: OrganizationList = OrganizationList()

        for _, row in df.iterrows():
            orgs.add_organization(Organization(o_id=row['id'], name=row['name']))
        
        return orgs
