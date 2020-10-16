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

from api_requester import ApiRequester


ORGANIZATION_QUERY: str = '{{organizations(first: {0}, skip: {1}\
){{id createdAt recoveryVault}}}}'

META_KEY: str = 'organizations'


def _request_organizations(current_rows: int) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.ARAGON_MAINNET)
    print("Requesting Organization\'s data ...")
    start: datetime = datetime.now()

    orgs: List[Dict] = requester.n_requests(query=ORGANIZATION_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Organization\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return orgs


def _transform_to_df(orgs: List[Dict], n_daos: int) -> pd.DataFrame:
    if not orgs:
        return pd.DataFrame()

    df: pd.DataFrame = pd.DataFrame(orgs)
    
    #TODO: temporal solution to non-attribute name
    names: List[str] = [f'Noname-{i+n_daos}' for i in range(len(df))]
    df['name'] = names

    return df


def update_organizations(meta_data: Dict) -> None:
    orgs: List[Dict] = _request_organizations(current_rows=meta_data[META_KEY]['rows'])
    df: pd.DataFrame = _transform_to_df(orgs=orgs, n_daos=meta_data[META_KEY]['rows'])

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(orgs)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_organizations(meta_data=meta)
