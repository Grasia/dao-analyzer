"""
   Descp: Tester for organization transfers.

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
import unittest
from hypothesis import given, example, settings, strategies as st
from random import Random

from dao_analyzer.web.apps.common.business.transfers.organization import Organization
from dao_analyzer.web.apps.common.business.transfers.organization import OrganizationList


OrganizationStrategy = st.builds(
    Organization,
    o_id=st.text(min_size=2),
    name=st.text())

ALL_ORGS_ID = OrganizationList.ALL_ORGS_ID

class OrganizationTest(unittest.TestCase):

    def test_get_dict_representation_1(self):
        org1: Organization = Organization(o_id='222', name='test2', network="n")
        org2: Organization = Organization(o_id='111', name='test1', network="n")
        orgs: OrganizationList = OrganizationList(orgs=[org1, org2])
        result: List[Dict[str, str]] = orgs.get_dict_representation()

        sol: List[Dict[str, str]] = [
            {'value': ALL_ORGS_ID, 'label': 'All DAOs'},
            {'value': '111', 'label': 'test1 (111... n)'},
            {'value': '222', 'label': 'test2 (222... n)'},
        ]

        for i, r in enumerate(result):
            self.assertEqual(sol[i]['value'], r['value'])
            self.assertEqual(sol[i]['label'], r['label'])


    @example(orgs=list())
    @given(orgs=st.lists(OrganizationStrategy))
    @settings(max_examples=30)
    def test_get_dict_representation_2(self, orgs):
        l_org: OrganizationList = OrganizationList(orgs=orgs)
        result: List[Dict[str, str]] = l_org.get_dict_representation()

        sol: int = len(orgs) + 1 if len(orgs) > 0 else 0

        self.assertEqual(sol, len(result))


    @given(orgs=st.lists(OrganizationStrategy, min_size=1))
    @settings(max_examples=30)
    def test_get_ids_from_id_1(self, orgs: List[Organization]):
        l_org: OrganizationList = OrganizationList(orgs=orgs)
        org: Organization = Random().choice(orgs)
        ids: List[str] = l_org.get_ids_from_id(org.get_id())

        self.assertEqual(1, len(ids))
        self.assertEqual(org.get_id(), ids[0])


    @example(orgs=list())
    @given(orgs=st.lists(OrganizationStrategy))
    @settings(max_examples=30)
    def test_get_ids_from_id_2(self, orgs: List[Organization]):
        l_org: OrganizationList = OrganizationList(orgs=orgs)
        ids: List[str] = l_org.get_ids_from_id(ALL_ORGS_ID)

        self.assertEqual(len(orgs), len(ids))


if __name__ == "__main__":
    unittest.main()
