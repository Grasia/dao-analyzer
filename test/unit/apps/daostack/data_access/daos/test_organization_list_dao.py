"""
   Descp: Tester for OrganizationListDao.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os
import unittest
import pandas as pd

from src.apps.daostack.data_access.daos.organization_dao import OrganizationListDao
from src.apps.daostack.business.transfers.organization import OrganizationList
from src.apps.daostack.data_access.requesters.cache_requester import CacheRequester

class DaoOrganizationListTest(unittest.TestCase):

    def test_get_organizations1(self):
        filename: str = os.path.join('datawarehouse', 'daostack', 'daos.csv')
        requester: CacheRequester = CacheRequester(src=filename)
        dao: OrganizationListDao = OrganizationListDao(requester=requester)

        orgs: OrganizationList = dao.get_organizations()
        df: pd.DataFrame = requester.request()

        self.assertEqual(len(df), orgs.get_size())


    def test_get_organizations2(self):
        filename: str = os.path.join('datawarehouse', 'daostack', 'daos.csv')
        requester: CacheRequester = CacheRequester(src=filename)
        dao: OrganizationListDao = OrganizationListDao(requester=requester)

        orgs: OrganizationList = dao.get_organizations()
        df: pd.DataFrame = requester.request()
        df.set_index('id', inplace=True)

        for org in orgs.get_organizations():
            self.assertIn(org.get_id(), df.index)
            self.assertEqual(org.get_name(), df.loc[org.get_id(), 'name'])


if __name__ == "__main__":
    unittest.main()
