"""
   Descp: Script to fetch vote's data and store it as a caché.

   Created on: 29-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


VOTE_QUERY: str = '{{votes(first: {0}, skip: {1}\
){{id createdAt proposal{{id}} molochAddress memberAddress uintVote }}}}'

META_KEY: str = 'votes'


def _request_votes(current_rows: int) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.DAOHAUS)
    print("Requesting votes\'s data ...")
    start: datetime = datetime.now()

    data: List[Dict] = requester.n_requests(query=VOTE_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'votes\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return data


def _transform_to_df(data: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for d in data:
        proposal: str = d['proposal']['id']

        del d['proposal']

        d['proposalAddress'] = proposal

    return pd.DataFrame(data)


def update_votes(meta_data: Dict) -> None:
    data: List[Dict] = _request_votes(current_rows=meta_data[META_KEY]['rows'])
    df: pd.DataFrame = _transform_to_df(data=data)

    filename: str = os.path.join('datawarehouse', 'daohaus', 'votes.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(data)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_votes(meta_data=meta)
