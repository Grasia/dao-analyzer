"""
   Descp: Script to fetch TokenHolder's data and store it.

   Created on: 15-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester
from aragon.collectors.mini_me_token import META_KEY as TOKEN_KEY


TOKEN_HOLDER_QUERY: str = '{{tokenHolders(first: {0}, skip: {1}\
){{id address tokenAddress balance}}}}'

TOKEN_QUERY: str = '{{miniMeTokens(first: {0}, skip: {1}\
){{address orgAddress}}}}'

META_KEY: str = 'tokenHolders'


def _request_token_holders(current_rows: int) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.ARAGON_TOKENS)
    print("Requesting Token Holders\'s data ...")
    start: datetime = datetime.now()

    holders: List[Dict] = requester.n_requests(query=TOKEN_HOLDER_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Token Holders\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return holders


def _transform_to_df(holders: List[Dict]) -> pd.DataFrame:
    if not holders:
        return pd.DataFrame()

    df: pd.DataFrame = pd.DataFrame(holders)

    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.ARAGON_TOKENS)
    tokens: List[Dict] = requester.n_requests(
        query=TOKEN_QUERY, 
        skip_n=0, 
        result_key=TOKEN_KEY)

    # List[Dict[str, str]] -> Dict[str, str]
    tokens: Dict[str, str] = {token['address']: token['orgAddress'] for token in tokens}

    tokenAddreses: List[str] = df['tokenAddress'].tolist()
    orgAddrs: List[str] = [tokens[x] for x in tokenAddreses]

    df['organizationAddress'] = orgAddrs
    return df


def update_holders(meta_data: Dict) -> None:
    holders: List[Dict] = _request_token_holders(current_rows=meta_data[META_KEY]['rows'])
    df: pd.DataFrame = _transform_to_df(holders=holders)

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(holders)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_holders(meta_data=meta)
