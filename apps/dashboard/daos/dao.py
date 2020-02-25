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
import pandas as pd
from pandas.tseries.offsets import DateOffset
from datetime import datetime

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
    if not 'daos' in daos:
        return list()
    
    return daos['daos']


def get_reputation_holders(id: str) -> List[int]:
    """
    Gets a specific DAO's members.
    Params:
        id: the id of an existing DAO
    Return:
        A list filled with a timestamp(Unix time) for each member.
        If an error occurred, returns an empty list.
    """
    query: str = '''
    {
        dao(id: "''' + id + '''") {
            reputationHolders {
                createdAt
            }
        }
    }
    '''
    dao: Dict[str, List] = request(query)
    if not 'dao' in dao:
        return list()

    df: pd.DataFrame = pd.DataFrame([int(mem['createdAt']) 
        for mem in dao['dao']['reputationHolders']])

    df.columns = ['date']

    # takes just the month
    df['date'] = pd.to_datetime(df['date'], unit='s').dt.to_period('M')

    # counts how many month/year are repeated
    df = df.groupby(df['date']).size().reset_index(name='count')
    df['date'] = df['date'].dt.to_timestamp()
    
    # generates a time series
    start = df['date'].min()
    end = datetime.now()
    idx = pd.date_range(start=start, end=end, freq=DateOffset(months=1))

    # joinning all the data in a unique dataframe
    dff = pd.DataFrame({'date': idx})
    dff['count'] = 0
    df = df.append(dff).sort_values('date').reset_index(drop=True)
    df = df.drop_duplicates(subset='date', keep="first")

    result: Dict[str, List[pd.Timestamp]] = {
        'x': df['date'].tolist(),
        'y': df['count'].tolist(),
    }

    return result 