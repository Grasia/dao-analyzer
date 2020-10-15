"""
   Descp: Script to fetch MiniMeToken's data and store it.

   Created on: 15-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


MINI_ME_TOKEN_QUERY: str = '{{miniMeTokens(first: {0}, skip: {1}\
){{id address totalSupply transferable name symbol orgAddress appAddress}}}}'

META_KEY: str = 'miniMeTokens'


def _request_mini_me_tokens(current_rows: int) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.ARAGON_TOKENS)
    print("Requesting Mini me token\'s data ...")
    start: datetime = datetime.now()

    tokens: List[Dict] = requester.n_requests(query=MINI_ME_TOKEN_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Mini me token\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return tokens


def _transform_to_df(tokens: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(tokens)


def update_tokens(meta_data: Dict) -> None:
    tokens: List[Dict] = _request_mini_me_tokens(current_rows=meta_data[META_KEY]['rows'])
    df: pd.DataFrame = _transform_to_df(tokens=tokens)

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(tokens)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_tokens(meta_data=meta)
