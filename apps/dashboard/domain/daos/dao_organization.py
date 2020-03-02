"""
   Descp: This is a dao (data access object) of the organization.
    It's used in order to warp the transformation among
    API's responses and the App's transfer.  

   Created on: 24-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict
from datetime import datetime

import api.api_manager as api
from apps.dashboard.domain.transfers import Organization
from api.query_builder import QueryBuilder
from api.query import Query

from app import DEBUG
from logs import LOGS

def get_all_orgs() -> List[Organization]:
    """
    Requests all organizations.
    Return:
        A list filled with "Organization"s
    """
    orgs = list()
    chunk: int = 0
    result: Dict = dict()
    start: datetime = datetime.now()

    while chunk == 0 or ('daos' in result 
    and len(result['daos']) == api.get_elems_per_chunk(chunk - 1)):

        q_builder: QueryBuilder = QueryBuilder()
        query: Query = Query(header = 'daos', 
                             body = ['id', 'name'], 
                             filters = {
                                'where': '{register: \"registered\"}',
                                'first': f'{api.get_elems_per_chunk(chunk)}',
                                'skip' : f'{len(orgs)}',
                             })
        q_builder.add_query(query)
        result = api.request(q_builder.build())
        chunk += 1
    
        for ele in result['daos']:
            orgs.append(Organization(o_id=ele['id'], name=ele['name']))

    if DEBUG:
        print(LOGS['chunks_requested'].format(chunk, (datetime.now() - start)\
         .total_seconds() * 1000))
    
    return orgs