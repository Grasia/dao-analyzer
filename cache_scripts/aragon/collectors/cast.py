"""
   Descp: Script to fetch Cast data and store it. Cast means vote.

   Created on: 16-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


CAST_QUERY: str = '{{casts(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id vote {{id}} voter {{id}} supports stake createdAt vote{{orgAddress appAddress}} }}}}'

META_KEY: str = 'casts'


def _request_casts(current_row: int, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting Cast data ...")
    start: datetime = datetime.now()

    casts: List[Dict] = requester.n_requests(query=CAST_QUERY, skip_n=current_row, 
        result_key=META_KEY)

    print(f'Cast data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return casts


def _transform_to_df(casts: List[Dict]) -> pd.DataFrame:
    for cast in casts:
        org: str = cast['vote']['orgAddress']
        app: str = cast['vote']['appAddress']
        voteId: str = cast['vote']['id']
        voterId: str = cast['voter']['id']

        del cast['vote']
        del cast['voter']
        
        cast['orgAddress'] = org
        cast['appAddress'] = app
        cast['voteId'] = voteId
        cast['voter'] = voterId

    return pd.DataFrame(casts)


def update_casts(meta_data: Dict, net: str, endpoints: Dict) -> None:
    casts: List[Dict] = _request_casts(
        current_row=meta_data[net][META_KEY]['rows'],
        endpoint=endpoints[net]['aragon_voting'])

    df: pd.DataFrame = _transform_to_df(casts=casts)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(casts)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
