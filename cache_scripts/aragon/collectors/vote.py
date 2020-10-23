"""
   Descp: Script to fetch vote data and store it. 
    In Aragon context, Vote means proposal, and cast means vote.

   Created on: 16-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


VOTE_QUERY: str = '{{votes(first: {0}, skip: {1})\
{{id orgAddress appAddress creator metadata executed executedAt startDate \
supportRequiredPct minAcceptQuorum yea nay voteNum votingPower}}}}'

META_KEY: str = 'votes'


def _request_votes() -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.ARAGON_VOTING)
    print("Requesting Vote data ...")
    start: datetime = datetime.now()

    votes: List[Dict] = requester.n_requests(query=VOTE_QUERY, skip_n=0, 
        result_key=META_KEY)

    print(f'Vote data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return votes


def _transform_to_df(votes: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(votes)


def update_votes(meta_data: Dict) -> None:
    votes: List[Dict] = _request_votes()
    df: pd.DataFrame = _transform_to_df(votes=votes)

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    # Always rewrite the whole file cause it is more efficient to do it than request all the open proposals.
    df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = len(votes)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_votes(meta_data=meta)
