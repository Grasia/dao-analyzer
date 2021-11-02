"""
   Descp: Script to fetch Transaction's data and store it.

   Created on: 16-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


TRANSACTION_QUERY: str = '{{transactions(first: {first}, where: {{ id_gt: "{last_id}" }}\
){{id orgAddress appAddress token entity isIncoming amount date reference }}}}'

META_KEY: str = 'transactions'


def _request_transactions(last_id: str, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting Transaction's data ...")
    start: datetime = datetime.now()

    transactions: List[Dict] = requester.n_requests(query=TRANSACTION_QUERY, last_id=last_id, 
        result_key=META_KEY)

    print(f'Transaction\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return transactions


def _transform_to_df(transactions: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(transactions)


def update_transactions(meta_data: Dict, net: str, endpoints: Dict) -> None:
    transactions: List[Dict] = _request_transactions(
        last_id=meta_data[net][META_KEY]['last_id'],
        endpoint=endpoints[net]['aragon_finance'])

    df: pd.DataFrame = _transform_to_df(transactions=transactions)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(transactions)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
    meta_data[net][META_KEY]['last_id'] = transactions[-1]['id'] if transactions else ""
