"""
   Descp: Tester for API manager.

   Created on: 10-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List
import unittest

import src.api.api_manager as api

class ApiManagerTest(unittest.TestCase):
    def test_request_1(self):
        query: str = '{test}'
        result = api.request(query)
        self.assertEqual(0, len(result), 
            f'Expected result len = 0, but was {len(result)}')


    def test_request_2(self):
        query: str = '{daos(first: 5){name}}'
        result = api.request(query)
        l: int = len(result['daos'])
        self.assertEqual(5, l, 
            f'Expected len(result[\'daos\']) = 5, but was {l}')

    
    def test_get_elems_per_chunk(self):
        param: List[int] = [-1, 0, 1, 2, 10]
        sol: List[int] = [api.ELEMS_PER_CHUNK/2, api.ELEMS_PER_CHUNK, 
            2*api.ELEMS_PER_CHUNK, 4*api.ELEMS_PER_CHUNK, 1000]

        for i, p in enumerate(param):
            self.assertEqual(sol[i], api.get_elems_per_chunk(p))


if __name__ == "__main__":
    unittest.main()