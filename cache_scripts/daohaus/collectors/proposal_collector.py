"""
   Descp: Script to fetch proposal's data and store it as a caché.

   Created on: 29-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


PROPOSAL_QUERY: str = '{{proposals(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id createdAt proposalId molochAddress memberAddress proposer sponsor \
sharesRequested lootRequested tributeOffered paymentRequested yesVotes noVotes \
sponsored sponsoredAt processed didPass yesShares noShares}}}}'

O_PROPOSAL_QUERY: str = '{{proposal(id: \"{id}\")\
{{id createdAt proposalId molochAddress memberAddress proposer sponsor \
sharesRequested lootRequested tributeOffered paymentRequested yesVotes noVotes \
sponsored sponsoredAt processed didPass yesShares noShares}}}}'

META_KEY: str = 'proposals'


def _request_proposals(current_rows: int, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting proposal\'s data ...")
    start: datetime = datetime.now()

    data: List[Dict] = requester.n_requests(query=PROPOSAL_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'proposal\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return data


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


def _transform_to_df(data: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(data)


def _get_opened_proposals(df: pd.DataFrame, network: str) -> List[str]:
    dff: pd.DataFrame = df[df['network'] == network]
    dff = dff[dff['processed'] == False] # noqa: E72
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

    data: List[Dict] = _request_proposals(
        current_rows=meta_data[net][META_KEY]['rows'],
        endpoint=endpoints[net]['daohaus'])

    df3: pd.DataFrame = _transform_to_df(data=data)
    df3['network'] = net
    size: int = len(df3)

    filename: str = os.path.join('datawarehouse', 'daohaus', 'proposals.csv')

    # fetch new proposals and update opened proposals
    if os.path.isfile(filename):
        df = pd.read_csv(filename, header=0)

        open_prop: List[Dict] = _request_open_proposals(
            ids=_get_opened_proposals(df, net),
            endpoint=endpoints[net]['daohaus'])
        df2: pd.DataFrame = pd.DataFrame(open_prop)
        df2['network'] = net

        df = join_data(df=df, df2=df2, df3=df3)
        df.to_csv(filename, index=False)
        size = len(df3) + len(df2)

    # save all proposals
    else:
        df3.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = size
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
