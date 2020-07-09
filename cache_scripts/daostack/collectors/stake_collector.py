import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import n_requests


STAKE_QUERY: str = '{{proposalStakes(first: {0}, skip: {1})\
{{id createdAt staker outcome amount dao{{id}} proposal{{id}}}}}}'

META_KEY: str = 'proposalStakes'


def _request_stakes(current_rows: int) -> List[Dict]:
    print("Requesting stakes\'s data ...")
    start: datetime = datetime.now()

    stakes: List[Dict] = n_requests(query=STAKE_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Stake\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return stakes


def _transform_to_df(stakes: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for s in stakes:
        dao: str = s['dao']['id']
        proposal: str = s['proposal']['id']

        del s['dao']
        del s['proposal']

        s['dao'] = dao
        s['proposal'] = proposal

    return pd.DataFrame(stakes)


def update_stakes(meta_data: Dict) -> None:
    stakes: List[Dict] = _request_stakes(current_rows=
        meta_data[META_KEY]['rows'])

    df: pd.DataFrame = _transform_to_df(stakes=stakes)

    filename: str = os.path.join('datawarehouse', 'daostack', 'stakes.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(stakes)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_stakes(meta_data=meta)
