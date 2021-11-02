"""
   Descp: Script to fetch DAO's data and store it as a caché.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


DAO_QUERY: str = '{{daos(where: {{register: "registered", id_gt: "{last_id}" }}, first: {first}\
){{id name nativeToken{{id}} nativeReputation{{id}}}}}}'

META_KEY: str = 'daos'


def _request_daos(last_id: str, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting DAO\'s data ...")
    start: datetime = datetime.now()

    daos: List[Dict] = requester.n_requests(query=DAO_QUERY, last_id=last_id, 
        result_key=META_KEY)

    print(f'DAO\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return daos


def _transform_to_df(daos: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for d in daos:
        token: str = d['nativeToken']['id']
        rep: str = d['nativeReputation']['id']

        del d['nativeToken']
        del d['nativeReputation']

        d['nativeToken'] = token
        d['nativeReputation'] = rep

    return pd.DataFrame(daos)


def update_daos(meta_data: Dict, net: str, endpoints: Dict) -> None:
    daos: List[Dict] = _request_daos(
        last_id=meta_data[net][META_KEY]['last_id'],
        endpoint=endpoints[net]['daostack']
    )
    df: pd.DataFrame = _transform_to_df(daos=daos)
    df['network'] = net # add name of network

    filename: str = os.path.join('datawarehouse', 'daostack', 'daos.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(daos)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
    meta_data[net][META_KEY]['last_id'] = daos[-1]['id'] if daos else ""
