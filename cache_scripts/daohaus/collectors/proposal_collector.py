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


PROPOSAL_QUERY: str = '{{proposals(first: {0}, skip: {1}\
){{id createdAt proposalId molochAddress memberAddress proposer sponsor \
sharesRequested lootRequested tributeOffered paymentRequested yesVotes noVotes \
sponsored sponsoredAt processed didPass yesShares noShares}}}}'

O_PROPOSAL_QUERY: str = '{{proposal(id: \"{0}\")\
{{id yesVotes noVotes sponsor sponsored sponsoredAt processed didPass yesShares \
noShares}}}}'

META_KEY: str = 'proposals'


def _request_proposals(current_rows: int) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.DAOHAUS)
    print("Requesting proposal\'s data ...")
    start: datetime = datetime.now()

    data: List[Dict] = requester.n_requests(query=PROPOSAL_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'proposal\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return data


def _request_open_proposals(ids: List[str]) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.DAOHAUS)
    print("Requesting open proposals ...")
    start: datetime = datetime.now()

    open_props: List = list()
    result: Dict = list()
    try:
        for p_id in ids:
            query: str = O_PROPOSAL_QUERY.format(p_id)
            result = requester.request(query=query)
            open_props.append(result['proposal'])
    except Exception:
        print('\nError: Open proposals not updated.\n')

    print(f'Open proposals requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return open_props


def _transform_to_df(data: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(data)


def _get_opened_proposals(df: pd.DataFrame) -> List[str]:
    dff: pd.DataFrame = df[df['processed'] == False] # noqa: E72
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

    data: List[Dict] = _request_proposals(current_rows=meta_data[META_KEY]['rows'])
    
    df3: pd.DataFrame = _transform_to_df(data=data)

    filename: str = os.path.join('datawarehouse', 'daohaus', 'proposals.csv')

    # fetch new proposals and update opened proposals
    if os.path.isfile(filename):
        df = pd.read_csv(filename, header=0)

        open_prop: List[Dict] = _request_open_proposals(ids=_get_opened_proposals(df))
        df2: pd.DataFrame = pd.DataFrame(open_prop)

        df = join_data(df=df, df2=df2, df3=df3)
        df.to_csv(filename)

    # save all proposals
    else:
        df3.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(data)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_proposals(meta_data=meta)
