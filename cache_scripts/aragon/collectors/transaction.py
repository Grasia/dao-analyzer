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


TRANSACTION_QUERY: str = '{{transactions(first: {0}, skip: {1}\
){{id orgAddress appAddress token entity isIncoming amount date reference }}}}'

META_KEY: str = 'transactions'


def _request_transactions(current_rows: int) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=ApiRequester.ARAGON_FINANCE)
    print("Requesting Transaction's data ...")
    start: datetime = datetime.now()

    transactions: List[Dict] = requester.n_requests(query=TRANSACTION_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Transaction\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return transactions


def _transform_to_df(transactions: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(transactions)


def update_transactions(meta_data: Dict) -> None:
    transactions: List[Dict] = _request_transactions(current_rows=meta_data[META_KEY]['rows'])
    df: pd.DataFrame = _transform_to_df(transactions=transactions)

    filename: str = os.path.join('datawarehouse', 'aragon', f'{META_KEY}.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(transactions)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_transactions(meta_data=meta)
