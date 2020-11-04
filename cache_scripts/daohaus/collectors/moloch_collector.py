"""
   Descp: Script to fetch MOLOCH's data and store it as a caché.

   Created on: 29-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import ApiRequester


MOLOCH_QUERY: str = '{{moloches(where: {{deleted: false}}, first: {0}, skip: {1}\
){{id title version totalShares totalLoot summoner summoningTime}}}}'

META_KEY: str = 'moloches'


def _request_moloches(current_row: int, endpoint: str) -> List[Dict]:
    requester: ApiRequester = ApiRequester(endpoint=endpoint)
    print("Requesting MOLOCH\'s data ...")
    start: datetime = datetime.now()

    moloches: List[Dict] = requester.n_requests(query=MOLOCH_QUERY, skip_n=current_row, 
        result_key=META_KEY)

    print(f'MOLOCH\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return moloches


def _transform_to_df(moloches: List[Dict]) -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame(moloches)
    df = df.rename(columns={'title':'name'})
    return df


def update_moloches(meta_data: Dict, net: str, endpoints: Dict) -> None:
    moloches: List[Dict] = _request_moloches(
        current_row=meta_data[net][META_KEY]['rows'],
        endpoint=endpoints[net]['daohaus'])

    df: pd.DataFrame = _transform_to_df(moloches=moloches)
    df['network'] = net

    filename: str = os.path.join('datawarehouse', 'daohaus', 'moloches.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.\n')

    # update meta
    meta_data[net][META_KEY]['rows'] = meta_data[net][META_KEY]['rows'] + len(moloches)
    meta_data[net][META_KEY]['lastUpdate'] = str(date.today())
