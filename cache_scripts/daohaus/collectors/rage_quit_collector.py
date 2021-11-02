"""
   Descp: Script to fetch rage-quitting's data and store it as a caché.

   Created on: 29-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


RAGE_QUIT_QUERY: str = '{{rageQuits(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id createdAt molochAddress memberAddress shares loot}}}}'

META_KEY: str = 'rageQuits'


def _request_rage_quits(last_id: str, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting rage quits\'s data ...")
    start: datetime = datetime.now()

    data: List[Dict] = requester.n_requests(query=RAGE_QUIT_QUERY, last_id=last_id, 
        result_key=META_KEY)

    print(f'rage quits\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return data


def _transform_to_df(data: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(data)


def update_rage_quits(meta_data: Dict, net: str, endpoints: Dict) -> None:
    data: List[Dict] = _request_rage_quits(
        last_id=meta_data[net][META_KEY]['last_id'],
        endpoint=endpoints[net]['daohaus'])

    df: pd.DataFrame = _transform_to_df(data=data)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'daohaus', 'rage_quits.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(data)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
    meta_data[net][META_KEY]['last_id'] = data[-1]['id'] if data else ""
