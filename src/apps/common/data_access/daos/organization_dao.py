"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 17-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
import pandas as pd

from src.apps.common.business.transfers.organization import Organization
from src.apps.common.business.transfers.organization import OrganizationList
from src.apps.common.data_access.requesters.irequester import IRequester


class OrganizationListDao:
    def __init__(self, requester: IRequester):
        self.__requester = requester


    def get_organizations(self) -> OrganizationList:
        df: pd.DataFrame = self.__requester.request()
        orgs: OrganizationList = OrganizationList()

        for _, row in df.iterrows():
            name: str = f"{row['name']} ({row['network']})"
            orgs.add_organization(Organization(o_id=row['id'], name=name))
        
        return orgs
