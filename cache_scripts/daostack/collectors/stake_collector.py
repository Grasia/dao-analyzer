"""
   Descp: Script to fetch stake's data and store it as a caché.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


STAKE_QUERY: str = '{{proposalStakes(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id createdAt staker outcome amount dao{{id}} proposal{{id}}}}}}'

META_KEY: str = 'proposalStakes'


def _request_stakes(current_row: int, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting stakes\'s data ...")
    start: datetime = datetime.now()

    stakes: List[Dict] = requester.n_requests(query=STAKE_QUERY, skip_n=current_row, 
        result_key=META_KEY)

    print(f'Stake\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return stakes


def _transform_to_df(stakes: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for s in stakes:
        dao: str = s['dao']['id']
        proposal: str = s['proposal']['id']

        del s['dao']
        del s['proposal']

        s['dao'] = dao
        s['proposal'] = proposal

    return pd.DataFrame(stakes)


def update_stakes(meta_data: Dict, net: str, endpoints: Dict) -> None:
    stakes: List[Dict] = _request_stakes(
        current_row=meta_data[net][META_KEY]['rows'],
        endpoint=endpoints[net]['daostack'])

    df: pd.DataFrame = _transform_to_df(stakes=stakes)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'daostack', 'stakes.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(stakes)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
