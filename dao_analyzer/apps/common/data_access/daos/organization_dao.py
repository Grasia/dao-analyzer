"""
   Descp: This is a dao (data access object) of the organization.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 17-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List
import pandas as pd

from dao_analyzer.apps.common.business.transfers.organization import Organization
from dao_analyzer.apps.common.business.transfers.organization import OrganizationList
from dao_analyzer.apps.common.data_access.requesters.irequester import IRequester


class OrganizationListDao:
    # Daohaus, Aragon
    __DATE_ROWS = ['summoningTime', 'createdAt']
    
    def __init__(self, requester: IRequester):
        self.__requester = requester


    def get_organizations(self) -> OrganizationList:
        df: pd.DataFrame = self.__requester.request()
        list: List[Organization] = []

        # Detect the time row
        date_idx = next((x for x in self.__DATE_ROWS if x in df.columns), None)

        # TODO: Optimize this somehow
        for _, row in df.iterrows():
            name = row['name'] if not pd.isna(row['name']) else None
            network = row['network'] if not pd.isna(row['network']) else None

            if date_idx and not pd.isna(row[date_idx]):
                creation_date = pd.to_datetime(row[date_idx], unit='s').date()
            else:
                creation_date = None

            list.append(Organization(o_id=row['id'], name=name, network=network, creation_date=creation_date))

        return OrganizationList(list)
