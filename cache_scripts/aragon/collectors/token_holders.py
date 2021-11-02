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


TOKEN_HOLDER_QUERY: str = '{{tokenHolders(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id address tokenAddress balance}}}}'

TOKEN_QUERY: str = '{{miniMeTokens(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id address orgAddress}}}}'

META_KEY: str = 'tokenHolders'


def _request_token_holders(last_id: str, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting Token Holders\'s data ...")
    start: datetime = datetime.now()

    holders: List[Dict] = requester.n_requests(query=TOKEN_HOLDER_QUERY, last_id=last_id, 
        result_key=META_KEY)

    print(f'Token Holders\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return holders


def _transform_to_df(holders: List[Dict], endpoint: str) -> pd.DataFrame:
    if not holders:
        return pd.DataFrame()

    df: pd.DataFrame = pd.DataFrame(holders)

    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    tokens: List[Dict] = requester.n_requests(
        query=TOKEN_QUERY, 
        last_id="", 
        result_key=TOKEN_KEY)

    # List[Dict[str, str]] -> Dict[str, str]
    tokens: Dict[str, str] = {token['address']: token['orgAddress'] for token in tokens}

    tokenAddreses: List[str] = df['tokenAddress'].tolist()
    orgAddrs: List[str] = [tokens[x] for x in tokenAddreses]

    df['organizationAddress'] = orgAddrs
    return df


def update_holders(meta_data: Dict, net: str, endpoints: Dict) -> None:
    holders: List[Dict] = _request_token_holders(
        last_id=meta_data[net][META_KEY]['last_id'],
        endpoint=endpoints[net]['aragon_tokens'])

    df: pd.DataFrame = _transform_to_df(
        holders=holders,
        endpoint=endpoints[net]['aragon_tokens'])
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(holders)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
    meta_data[net][META_KEY]['last_id'] = holders[-1]['id'] if holders else ""
