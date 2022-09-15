"""
   Descp: ApiRequester mock up for testing

   Created on: 14-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from typing import Any, List, Dict
from dao_analyzer.web.apps.common.data_access.requesters.irequester import IRequester

class ApiRequesterMock(IRequester):
    def __init__(self, any_list: List[Dict]):
        self.call_times: int = 0
        self.any_list: List[Dict] = any_list


    def request(self, any: Any) -> Dict:
        result = self.any_list[self.call_times]

        if self.call_times < len(self.any_list)-1:
            self.call_times += 1

        return result


    def get_elems_per_chunk(self, n_chunk: int) -> int:
        return pow(2, n_chunk)
