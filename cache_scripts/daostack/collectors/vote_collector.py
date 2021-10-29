"""
   Descp: Script to fetch vote's data and store it as a caché.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester

VOTE_QUERY: str = '{{proposalVotes(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id createdAt voter outcome reputation dao{{id}} proposal{{id}}}}}}'

META_KEY: str = 'proposalVotes'


def _request_votes(current_row: int, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting votes\'s data ...")
    start: datetime = datetime.now()

    votes: List[Dict] = requester.n_requests(query=VOTE_QUERY, skip_n=current_row, 
        result_key=META_KEY)

    print(f'Votes\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return votes


def _transform_to_df(votes: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for v in votes:
        dao: str = v['dao']['id']
        proposal: str = v['proposal']['id']

        del v['dao']
        del v['proposal']

        v['dao'] = dao
        v['proposal'] = proposal

    return pd.DataFrame(votes)


def update_votes(meta_data: Dict, net: str, endpoints: Dict) -> None:
    votes: List[Dict] = _request_votes(
        current_row=meta_data[net][META_KEY]['rows'],
        endpoint=endpoints[net]['daostack'])

    df: pd.DataFrame = _transform_to_df(votes=votes)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'daostack', 'votes.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(votes)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
