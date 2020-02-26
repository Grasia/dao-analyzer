"""
   Descp: This is a dao (data access object) of the organization.
    It's used in order to warp the transformation among
    API's responses and the App's transfer.  

   Created on: 24-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict

from api_manager import request
from apps.dashboard.domain.model_transfers import Organization

def get_all_orgs() -> List[Organization]:
    """
    Requests all organizations.
    Return:
        A list filled with "Organization"s
    """
    orgs = list()
    query: str = '''
    {
        daos(where: {register: "registered"}) {
            id
            name
        }
    }
    '''
    result: Dict = request(query)
    if 'daos' in result:
        for ele in result['daos']:
            orgs.append(Organization(o_id=ele['id'], name=ele['name']))
    
    return orgs