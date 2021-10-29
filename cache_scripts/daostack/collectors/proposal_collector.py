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

from api_requester import ApiRequester


PROPOSAL_QUERY: str = '{{proposals(first: {first}, where: {{ id_gt: "{last_id}" }})\
{{id proposer stage createdAt preBoostedAt boostedAt closingAt executedAt \
totalRepWhenExecuted totalRepWhenCreated executionState \
expiresInQueueAt votesFor votesAgainst winningOutcome stakesFor stakesAgainst \
genesisProtocolParams{{queuedVoteRequiredPercentage}} dao{{id}} }}}}'

O_PROPOSAL_QUERY: str = '{{proposal(id: "{id}")\
{{id proposer stage createdAt preBoostedAt boostedAt closingAt executedAt \
totalRepWhenExecuted totalRepWhenCreated executionState \
expiresInQueueAt votesFor votesAgainst winningOutcome stakesFor stakesAgainst \
genesisProtocolParams{{queuedVoteRequiredPercentage}} dao{{id}} }}}}'

META_KEY: str = 'proposals'
OUT_FILE: str = os.path.join('datawarehouse', 'daostack', 'proposals.csv')


def _request_proposals(current_row: int, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting proposal\'s data ...")
    start: datetime = datetime.now()

    proposals: List[Dict] = requester.n_requests(query=PROPOSAL_QUERY, skip_n=current_row, 
        result_key=META_KEY)

    print(f'Proposal\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return proposals


def _request_open_proposals(ids: List[str], endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting open proposals ...")
    start: datetime = datetime.now()

    open_props: List = list()
    result: Dict = list()
    try:
        for p_id in ids:
            query: str = O_PROPOSAL_QUERY.format(id=p_id)
            result = requester.request(query=query)
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


def _get_opened_proposals(df: pd.DataFrame, network: str) -> List[str]:
    dff: pd.DataFrame = df[df['executedAt'].isnull()]
    dff = dff[dff['network'] == network]
    return dff['id'].tolist()


def join_data(df: pd.DataFrame, df2: pd.DataFrame, df3: pd.DataFrame) -> pd.DataFrame:
    """
        Updates df with df2, and apends df3 rows in df
    """
    dff: pd.DataFrame = df

    if len(df2) > 0:
        ids: List[str] = df2['id'].tolist()
        index = dff[dff['id'].isin(ids)].index
        dff.drop(index, inplace=True)
        dff = dff.append(df2)

    if len(df3) > 0:
        dff = dff.append(df3)

    return dff


def update_proposals(meta_data: Dict, net: str, endpoints: Dict) -> None:
    df: pd.DataFrame

    proposals: List[Dict] = _request_proposals(
        current_row=meta_data[net][META_KEY]['rows'],
        endpoint=endpoints[net]['daostack'])
    df3: pd.DataFrame = _transform_to_df(proposals=proposals)
    df3['network'] = net
    size: int = len(df3)

    # fetch new proposals and update opened proposals
    if os.path.isfile(OUT_FILE):
        df = pd.read_csv(OUT_FILE, header=0)

        open_prop: List[Dict] = _request_open_proposals(
            ids=_get_opened_proposals(df, network=net),
            endpoint=endpoints[net]['daostack'])
        df2: pd.DataFrame = _transform_to_df(proposals=open_prop)
        df2['network'] = net

        df = join_data(df=df, df2=df2, df3=df3)
        df.to_csv(OUT_FILE, index=False)
        size = len(df3) + len(df2)

    # save all proposals
    else:
        df3.to_csv(OUT_FILE, index=False)

    print(f'Data stored in {OUT_FILE}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = size
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
