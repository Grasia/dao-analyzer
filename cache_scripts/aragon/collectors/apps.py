"""
   Descp: Script to fetch app's data and store it.

   Created on: 15-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date
import logging

from api_requester import ApiRequester


APP_QUERY: str = '{{apps(first: {0}, skip: {1}\
){{id isForwarder isUpgradeable repoName repoAddress organization{{id}} }}}}'

META_KEY: str = 'apps'


def _request_apps(current_row: int, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting App\'s data ...")
    start: datetime = datetime.now()

    apps: List[Dict] = requester.n_requests(query=APP_QUERY, skip_n=current_row, 
        result_key=META_KEY)

    logging.info(f'App\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return apps


def _transform_to_df(apps: List[Dict]) -> pd.DataFrame:
    for app in apps:
        org: str = app['organization']['id']
        del app['organization']
        app['organizationId'] = org

    return pd.DataFrame(apps)


def update_apps(meta_data: Dict, net: str, endpoints: Dict) -> None:
    apps: List[Dict] = _request_apps(
        current_row=meta_data[net][META_KEY]['rows'],
        endpoint=endpoints[net]['aragon'])

    df: pd.DataFrame = _transform_to_df(apps=apps)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(apps)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
