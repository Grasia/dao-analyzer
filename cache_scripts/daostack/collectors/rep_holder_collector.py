"""
   Descp: Script to fetch users's data and store it as a caché.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


REP_HOLDER_QUERY: str = '{{reputationHolders(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id contract address balance createdAt dao{{id}}}}}}'

META_KEY: str = 'reputationHolders'


def _request_rep_holders(last_id: str, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting reputation holder\'s data ...")
    start: datetime = datetime.now()

    reps: List[Dict] = requester.n_requests(query=REP_HOLDER_QUERY, last_id=last_id, 
        result_key=META_KEY)

    print(f'Reputation holder\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return reps


def _transform_to_df(reps: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for r in reps:
        dao: str = r['dao']['id']
        del r['dao']
        r['dao'] = dao

    return pd.DataFrame(reps)


def update_rep_holders(meta_data: Dict, net: str, endpoints: Dict) -> None:
    reps: List[Dict] = _request_rep_holders(
        last_id=meta_data[net][META_KEY]['last_id'],
        endpoint=endpoints[net]['daostack'])

    df: pd.DataFrame = _transform_to_df(reps=reps)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'daostack', 
        'reputation_holders.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(reps)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
    meta_data[net][META_KEY]['last_id'] = reps[-1]['id'] if reps else ""
