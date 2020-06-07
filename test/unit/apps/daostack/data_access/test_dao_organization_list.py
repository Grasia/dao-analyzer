"""
   Descp: Tester for DaoOrganizationList.

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from hypothesis import given, settings, strategies as st
from typing import List, Dict

from src.apps.daostack.data_access.graphql.dao_organization import DaoOrganizationList
from src.apps.daostack.business.transfers.organization import OrganizationList
from test.mocks.request_mock import RequestMock


@st.composite
def custom_dictionary(draw, size: int) -> Dict:
    return draw(st.fixed_dictionaries({
                    'daos': st.lists(
                            st.fixed_dictionaries({
                                'id': st.text(),
                                'name': st.text(),
                            }),
                            min_size=size,
                            max_size=size)}))


class DaoOrganizationListTest(unittest.TestCase):
    @given(
        r1=custom_dictionary(size=1),
        r2=custom_dictionary(size=2), 
        r3=custom_dictionary(size=4),
        r4=custom_dictionary(size=2))
    @settings(max_examples=30)
    def test_get_organizations(self, r1: Dict, r2: Dict, r3: Dict, r4: Dict):
        results: List = [r1, r2, r3, r4]
        mock: RequestMock = RequestMock(any_list=results)
        dao: DaoOrganizationList = DaoOrganizationList(requester=mock)
        daos: OrganizationList = dao.get_organizations()

        sol: int = sum(len(x['daos']) for x in results)

        self.assertEqual(sol, daos.get_size())


if __name__ == "__main__":
    unittest.main()
