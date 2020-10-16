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


CAST_QUERY: str = '{{casts(first: {0}, skip: {1}\
){{id voteId voter supports voterStake createdAt vote{{orgAddress appAddress}} }}}}'

META_KEY: str = 'casts'


def _request_casts(current_rows: int) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.ARAGON_VOTING)
    print("Requesting Cast data ...")
    start: datetime = datetime.now()

    casts: List[Dict] = requester.n_requests(query=CAST_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Cast data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return casts


def _transform_to_df(casts: List[Dict]) -> pd.DataFrame:
    for cast in casts:
        org: str = cast['vote']['orgAddress']
        app: str = cast['vote']['appAddress']

        del cast['vote']
        
        cast['orgAddress'] = org
        cast['appAddress'] = app

    return pd.DataFrame(casts)


def update_casts(meta_data: Dict) -> None:
    casts: List[Dict] = _request_casts(current_rows=meta_data[META_KEY]['rows'])
    df: pd.DataFrame = _transform_to_df(casts=casts)

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(casts)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_casts(meta_data=meta)
