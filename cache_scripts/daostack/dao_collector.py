import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import n_requests


DAO_QUERY: str = '{{daos(where: {{register: "registered"}}, first: {0}, skip: {1}\
){{id name nativeToken{{id}} nativeReputation{{id}}}}}}'

META_KEY: str = 'daos'


def request_daos(current_rows: int) -> List[Dict]:
    print("Requesting DAO\'s data ...")
    start: datetime = datetime.now()

    daos: List[Dict] = n_requests(query=DAO_QUERY, skip_n=current_rows, result_key='daos')

    print(f'DAO\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return daos


def transform_to_df(daos: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for d in daos:
        token: str = d['nativeToken']['id']
        rep: str = d['nativeReputation']['id']

        del d['nativeToken']
        del d['nativeReputation']

        d['nativeToken'] = token
        d['nativeReputation'] = rep

    return pd.DataFrame(daos)


def update_daos(meta_data: Dict) -> None:
    daos: List[Dict] = request_daos(current_rows=int(meta_data[META_KEY]['rows']))
    df: pd.DataFrame = transform_to_df(daos=daos)

    filename: str = os.path.join('datawarehouse', 'daostack', 'daos.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.')

    # update meta
    meta_data[META_KEY]['rows'] = int(meta_data[META_KEY]['rows']) + len(daos)
    meta_data[META_KEY]['lastUpdate'] = date.today()


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_daos(meta_data=meta)
