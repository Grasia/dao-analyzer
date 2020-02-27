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

from api.api_manager import request
from apps.dashboard.domain.transfers import Organization
from api.query_builder import QueryBuilder
from api.query import Query
from api.api_manager import ELEMS_PER_CHUNK
from app import DEBUG
from logs import LOGS

def get_all_orgs() -> List[Organization]:
    """
    Requests all organizations.
    Return:
        A list filled with "Organization"s
    """
    orgs = list()
    chunks = 0
    result: Dict = dict()
    start: datetime = datetime.now()

    while chunks == 0 or ('daos' in result 
    and len(result['daos']) == ELEMS_PER_CHUNK):

        q_builder: QueryBuilder = QueryBuilder()
        query: Query = Query(header = 'daos', 
                             body = ['id', 'name'], 
                             filters = {
                                'where': '{register: \"registered\"}',
                                'first': f'{ELEMS_PER_CHUNK + ELEMS_PER_CHUNK * chunks}',
                                'skip' : f'{ELEMS_PER_CHUNK * chunks}',
                             })
        q_builder.add_query(query)
        result = request(q_builder.build())
        chunks += 1
    
        for ele in result['daos']:
            orgs.append(Organization(o_id=ele['id'], name=ele['name']))

    if DEBUG:
        print(LOGS['chunks_requested'].format(chunks, (datetime.now() - start)\
         .total_seconds() * 1000))
    
    return orgs