"""
   Descp: Script to fetch proposal's data and store it as a caché.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import n_requests, request


PROPOSAL_QUERY: str = '{{proposals(first: {0}, skip: {1})\
{{id proposer stage createdAt preBoostedAt boostedAt closingAt executedAt \
totalRepWhenExecuted totalRepWhenCreated executionState \
expiresInQueueAt votesFor votesAgainst winningOutcome stakesFor stakesAgainst \
genesisProtocolParams{{queuedVoteRequiredPercentage}} dao{{id}} }}}}'

O_PROPOSAL_QUERY: str = '{{proposal(id: \"{0}\")\
{{id stage preBoostedAt boostedAt executedAt totalRepWhenExecuted executionState \
expiresInQueueAt votesFor votesAgainst winningOutcome stakesFor stakesAgainst}}}}'

META_KEY: str = 'proposals'
OUT_FILE: str = os.path.join('datawarehouse', 'daostack', 'proposals.csv')


def _request_proposals(current_rows: int) -> List[Dict]:
    print("Requesting proposal\'s data ...")
    start: datetime = datetime.now()

    proposals: List[Dict] = n_requests(query=PROPOSAL_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Proposal\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return proposals


def _request_open_proposals(ids: List[str]) -> List[Dict]:
    print("Requesting open proposals ...")
    start: datetime = datetime.now()

    open_props: List = list()
    result: Dict = list()
    try:
        for p_id in ids:
            query: str = O_PROPOSAL_QUERY.format(p_id)
            result = request(query=query)
            open_props.append(result['proposal'])
    except Exception:
        print('\nError: Open proposals not updated.\n')

    print(f'Open proposals requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return open_props


def _transform_to_df(proposals: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for p in proposals:
        dao: str = p['dao']['id']
        per: str = p['genesisProtocolParams']['queuedVoteRequiredPercentage']

        del p['dao']
        del p['genesisProtocolParams']

        p['dao'] = dao
        p['queuedVoteRequiredPercentage'] = per

    return pd.DataFrame(proposals)


def _get_opened_proposals(df: pd.DataFrame) -> List[str]:
    dff: pd.DataFrame = df[df['executedAt'].isnull()]
    return dff['id'].tolist()


def join_data(df: pd.DataFrame, df2: pd.DataFrame, df3: pd.DataFrame) -> pd.DataFrame:
    """
        Updates df with df2, and apends df3 rows in df
    """
    dff: pd.DataFrame = df

    dff.set_index('id', inplace=True)

    if len(df2) > 0:
        df2.set_index('id', inplace=True)
        dff.update(df2)

    if len(df3) > 0:
        df3.set_index('id', inplace=True)
        dff = dff.append(df3)

    return dff


def update_proposals(meta_data: Dict) -> None:
    df: pd.DataFrame

    proposals: List[Dict] = _request_proposals(current_rows=
        meta_data[META_KEY]['rows'])
    df3: pd.DataFrame = _transform_to_df(proposals=proposals)

    # fetch new proposals and update opened proposals
    if os.path.isfile(OUT_FILE):
        df = pd.read_csv(OUT_FILE, header=0)

        open_prop: List[Dict] = _request_open_proposals(ids=_get_opened_proposals(df))
        df2: pd.DataFrame = pd.DataFrame(open_prop)

        df = join_data(df=df, df2=df2, df3=df3)
        df.to_csv(OUT_FILE)

    # save all proposals
    else:
        df3.to_csv(OUT_FILE, index=False)

    print(f'Data stored in {OUT_FILE}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(proposals)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_proposals(meta_data=meta)
