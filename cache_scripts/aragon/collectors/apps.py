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

from api_requester import ApiRequester


APP_QUERY: str = '{{apps(first: {0}, skip: {1}\
){{id isForwarder isUpgradeable repoName organization{{id}} }}}}'

META_KEY: str = 'apps'


def _request_apps(current_rows: int) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.ARAGON_MAINNET)
    print("Requesting App\'s data ...")
    start: datetime = datetime.now()

    apps: List[Dict] = requester.n_requests(query=APP_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'App\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return apps


def _transform_to_df(apps: List[Dict]) -> pd.DataFrame:
    for app in apps:
        org: str = app['organization']['id']
        del app['organization']
        app['organizationId'] = org

    return pd.DataFrame(apps)


def update_apps(meta_data: Dict) -> None:
    apps: List[Dict] = _request_apps(current_rows=meta_data[META_KEY]['rows'])
    df: pd.DataFrame = _transform_to_df(apps=apps)

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(apps)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_apps(meta_data=meta)
