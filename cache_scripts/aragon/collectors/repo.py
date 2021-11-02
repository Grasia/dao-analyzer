"""
   Descp: Script to fetch repo data and store it, app schema is an instances of repo.

   Created on: 16-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


REPO_QUERY: str = '{{repos(first: {first}, where: {{ id_gt: "{last_id}" }})\
    {{id address name node appCount}}}}'
META_KEY: str = 'repos'


def _request_repos(last_id: str, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting Repo data ...")
    start: datetime = datetime.now()

    repos: List[Dict] = requester.n_requests(query=REPO_QUERY, last_id=last_id, 
        result_key=META_KEY)

    print(f'Repo data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return repos


def _transform_to_df(repos: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(repos)


def update_repos(meta_data: Dict, net: str, endpoints: Dict) -> None:
    repos: List[Dict] = _request_repos(
        last_id=meta_data[net][META_KEY]['last_id'],
        endpoint=endpoints[net]['aragon'])

    df: pd.DataFrame = _transform_to_df(repos=repos)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(repos)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
    meta_data[net][META_KEY]['last_id'] = repos[-1]['id'] if repos else ""
