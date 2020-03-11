"""
   Descp: Unit tests for app_service

   Created on: 11-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import unittest
from unittest.mock import MagicMock
from typing import Any, List, Dict, Set
from hypothesis import given, example, settings, strategies as st

from src.apps.daostack.business.transfers.organization import Organization
from src.apps.daostack.business.app_service import Service


OrgStrategy = st.builds(
    Organization,
    o_id = st.text(),
    name = st.text(),
)


class ServiceTest(unittest.TestCase):
    @example(orgs=None)
    @given(orgs=st.lists(OrgStrategy))
    @settings(max_examples=30)
    def test_ids_generation(self, orgs: List[Organization]):
        mock = MagicMock(return_value=orgs)
        service = Service(dao_org=mock, dao_serie='error', dao_prop='error')
        service.get_layout()
        sol: Set[str] = set()
        if orgs:
            sol = {org.id for org in orgs}
            # 1 = ALL ORGS
            sol.add('1')
            for _id in service.get_ids():
                self.assertIn(_id, sol, f'{_id} is not in {sol}')


if __name__ == "__main__":
    unittest.main()
