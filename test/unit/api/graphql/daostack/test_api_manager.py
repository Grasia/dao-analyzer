"""
   Descp: Tester for API manager.

   Created on: 10-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
import unittest

from src.api.graphql.daostack.api_manager import ApiRequester

class ApiManagerTest(unittest.TestCase):
    """
    Unit tests for APIs should be smalls and as fast as possible, so, 
    do not request big chunks of data.
    """
    def test_request_1(self):
        query: str = '{test}'
        result = ApiRequester().request(query)
        self.assertEqual(0, len(result), 
            f'Expected result len = 0, but was {len(result)}')


    def test_request_2(self):
        query: str = '{daos(first: 2){name}}'
        result = ApiRequester().request(query)
        l: int = len(result['daos'])
        self.assertEqual(2, l, 
            f'Expected len(result[\'daos\']) = 2, but was {l}')

    
    def test_get_elems_per_chunk(self):
        param: List[int] = [-1, 0, 1, 2, 10]
        sol: List[int] = [50, 100, 200, 400, 1000]

        for i, p in enumerate(param):
            self.assertEqual(sol[i], ApiRequester().get_elems_per_chunk(p))


if __name__ == "__main__":
    unittest.main()