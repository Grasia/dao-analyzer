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


def get_new_users_data(id: str) -> Dict:
    """
    Gets a specific DAO's members.
    Params:
        id: the id of an existing DAO
    Return:
        A dict filled with:
            * x = a list with timestamps
            * y = a list with new users in a 'x' month
            * last_month_users = the number of users in the last month
            * last_month_name = the name of the last month
            * month_over_month = a percentage of how many users join among
                the last two months.
        If an error occurred, returns an empty dict.
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
        return dict()

    df: pd.DataFrame = pd.DataFrame([int(mem['createdAt']) 
        for mem in dao['dao']['reputationHolders']], columns = ['date'])

    # takes just the month
    df['date'] = pd.to_datetime(df['date'], unit='s').dt.to_period('M')

    # counts how many month/year are repeated
    df = df.groupby(df['date']).size().reset_index(name='count')
    df['date'] = df['date'].dt.to_timestamp()
    
    # generates a time series
    today = datetime.now()
    today = datetime(today.year, today.month, 1)
    start = df['date'].min() if len(df['date']) > 0 else today 
    end = today
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
    result['last_month_users'] = result['y'][-1]
    result['last_month_name'] = result['x'][-1].strftime('%B')

    if len(result['y']) < 2:
        result['month_over_month'] = 0
    else:
        divider: int = result['y'][-1] + result['y'][-2]
        if divider == 0:
            result['month_over_month'] = 0
        else:
            result['month_over_month'] = (result['y'][-1] - 
                result['y'][-2]) / divider * 100

    return result 