"""
   Descp: Tester for OrganizationListDao.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import unittest
from unittest.mock import MagicMock
import pandas as pd

from dao_analyzer.apps.common.data_access.daos.organization_dao import OrganizationListDao
from dao_analyzer.apps.common.business.transfers.organization import OrganizationList
from dao_analyzer.apps.common.data_access.requesters.cache_requester import CacheRequester

class DaoOrganizationListTest(unittest.TestCase):

    def __get_test_data(self) -> pd.DataFrame:
        return pd.DataFrame([
            {'id': '0', 'name': 'dao1', 'trash': 'trash', 'network': 'a'},
            {'id': '-1', 'name': 'dao-1', 'trash': 'trash', 'network': 'b'},
            {'id': '4', 'name': 'dao4', 'trash': 'trash', 'network': 'c'},
            {'id': '88pku88d8dd8d8', 'name': 'odd', 'trash': 'trash', 'network': 'a'},
        ])


    def test_get_organizations1(self):
        requester: CacheRequester = CacheRequester(srcs=[''])
        requester.request = MagicMock(return_value=self.__get_test_data())
        dao: OrganizationListDao = OrganizationListDao(requester=requester)

        orgs: OrganizationList = dao.get_organizations()
        df: pd.DataFrame = requester.request()

        self.assertEqual(len(df), orgs.get_size())


    def test_get_organizations2(self):
        requester: CacheRequester = CacheRequester(srcs=[''])
        requester.request = MagicMock(return_value=self.__get_test_data())
        dao: OrganizationListDao = OrganizationListDao(requester=requester)

        orgs: OrganizationList = dao.get_organizations()
        df: pd.DataFrame = requester.request()
        df = df.set_index('id')

        for org in orgs.get_organizations():
            self.assertIn(org.get_id(), df.index)
            name: str = df.loc[org.get_id(), 'name']
            self.assertEqual(org.get_name(), name)


if __name__ == "__main__":
    unittest.main()
