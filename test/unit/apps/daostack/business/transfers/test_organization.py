"""
   Descp: Tester for organization transfers.

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict
import unittest

from src.apps.daostack.business.transfers.organization import Organization
from src.apps.daostack.business.transfers.organization import OrganizationList

class OrganizationTest(unittest.TestCase):

    def test_get_dict_representation_1(self):
        org1: Organization = Organization(o_id='222', name='test2')
        org2: Organization = Organization(o_id='111', name='test1')
        orgs: OrganizationList = OrganizationList(orgs=[org1, org2])
        result = orgs.get_dict_representation()

        sol: List[Dict[str, str]] = [
            {'value': '1', 'label': 'All DAOs'},
            {'value': '111', 'label': 'test1'},
            {'value': '222', 'label': 'test2'},
        ]

        for i, r in enumerate(result):
            self.assertEqual(sol[i]['value'], r['value'])
            self.assertEqual(sol[i]['label'], r['label'])


if __name__ == "__main__":
    unittest.main()
