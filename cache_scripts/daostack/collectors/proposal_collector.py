import os
import pandas as pd
from typing import Dict, List
from datetime import datetime, date

from api_requester import n_requests


PROPOSAL_QUERY: str = '{{proposals(first: {0}, skip: {1})\
{{id proposer stage createdAt preBoostedAt boostedAt closingAt executedAt \
totalRepWhenExecuted totalRepWhenCreated executionState organizationId \
expiresInQueueAt votesFor votesAgainst winningOutcome stakesFor stakesAgainst \
genesisProtocolParams{{queuedVoteRequiredPercentage}}}}}}'

META_KEY: str = 'proposals'


def _request_proposals(current_rows: int) -> List[Dict]:
    print("Requesting proposal\'s data ...")
    start: datetime = datetime.now()

    proposals: List[Dict] = n_requests(query=PROPOSAL_QUERY, skip_n=current_rows, 
        result_key=META_KEY)

    print(f'Proposal\'s data requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return proposals


def _transform_to_df(proposals: List[Dict]) -> pd.DataFrame:
    # remove neasted dicts
    for p in proposals:
        dao: str = p['organizationId']
        per: str = p['genesisProtocolParams']['queuedVoteRequiredPercentage']

        del p['organizationId']
        del p['genesisProtocolParams']

        p['dao'] = dao
        p['queuedVoteRequiredPercentage'] = per

    return pd.DataFrame(proposals)


def update_proposals(meta_data: Dict) -> None:
    proposals: List[Dict] = _request_proposals(current_rows=
        meta_data[META_KEY]['rows'])

    df: pd.DataFrame = _transform_to_df(proposals=proposals)

    filename: str = os.path.join('datawarehouse', 'daostack', 'proposals.csv')

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False)
    else:
        df.to_csv(filename, index=False)

    print(f'Data stored in {filename}.')

    # update meta
    meta_data[META_KEY]['rows'] = meta_data[META_KEY]['rows'] + len(proposals)
    meta_data[META_KEY]['lastUpdate'] = str(date.today())


if __name__ == '__main__':
    meta: dict = {META_KEY: {'rows': 0}}
    update_proposals(meta_data=meta)
