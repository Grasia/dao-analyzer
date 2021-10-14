"""
   Descp: Script to fetch organization's data and store it.

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


ORGANIZATION_QUERY: str = '{{organizations(first: {0}, skip: {1}\
){{id createdAt recoveryVault}}}}'

META_KEY: str = 'organizations'


def _request_organizations(current_row: int, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting Organization\'s data ...")
    start: datetime = datetime.now()

    orgs: List[Dict] = requester.n_requests(query=ORGANIZATION_QUERY, skip_n=current_row, 
        result_key=META_KEY)

    logging.debug(f'Organization\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return orgs


def _transform_to_df(orgs: List[Dict]) -> pd.DataFrame:
    if not orgs:
        return pd.DataFrame()

    df: pd.DataFrame = pd.DataFrame(orgs)
    
    df['name'] = pd.NA

    return df


def update_organizations(meta_data: Dict, net: str, endpoints: Dict) -> None:
    orgs: List[Dict] = _request_organizations(
        current_row=meta_data[net][META_KEY]['rows'],
        endpoint=endpoints[net]['aragon'])

    df: pd.DataFrame = _transform_to_df(orgs=orgs)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    logging.debug(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(orgs)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
