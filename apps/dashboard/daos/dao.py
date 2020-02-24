"""
   dao.py

   Descp: This a dao (data access object) of a dao (decentralized autonomous
    organization). It's used in order to warp the transformation among
    API's responses and the App's object.  

   Created on: 24-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict

from api_manager import request

def get_all_daos() -> List[Dict[str, str]]:
    """
    Requests all the DAOs id-name
    Return:
        A list filled with DAOs dict -> key: id, value: name
    """
    query: str = '''
    {
        daos {
            id
            name
        }
    }
    '''
    daos: Dict[str, List] = request(query)
    return daos['daos']