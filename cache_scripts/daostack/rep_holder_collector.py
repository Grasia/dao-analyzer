import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import n_requests


REP_HOLDER_QUERY: str = '{{reputationHolders(first: {0}, skip: {1})\
{{id contract address balance createdAt dao{{id}}}}}}'

META_KEY: str = 'reputationHolders'


def _request_rep_holders(current_rows: int) -> List[Dict]:
    print("Requesting reputation holder\'s data ...")
    start: datetime = datetime.now()

    reps: List[Dict] = n_requests(query=REP_HOLDER_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Reputation holder\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return reps


def _transform_to_df(reps: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for r in reps:
        dao: str = r['dao']['id']
        del r['dao']
        r['dao'] = dao

    return pd.DataFrame(reps)


def update_rep_holders(meta_data: Dict) -> None:
    reps: List[Dict] = _request_rep_holders(current_rows=
        meta_data[META_KEY]['rows'])

    df: pd.DataFrame = _transform_to_df(reps=reps)

    filename: str = os.path.join('datawarehouse', 'daostack', 
        'reputation_holders.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(reps)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_rep_holders(meta_data=meta)
