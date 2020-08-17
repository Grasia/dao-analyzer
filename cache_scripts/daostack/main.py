"""
   Descp: Main script to create the app's caché, it call all the collectors.

   Created on: 10-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

import os
import json
from typing import Dict, List
import collectors.dao_collector as dao
import collectors.rep_holder_collector as rep_h
import collectors.vote_collector as vote
import collectors.stake_collector as stake
import collectors.proposal_collector as proposal

DIRS: str = os.path.join('datawarehouse', 'daostack')
META_PATH: str = os.path.join(DIRS, 'meta.json')


def _fill_empty_keys(meta_data: Dict) -> Dict:
    meta_fill: Dict = meta_data
    keys: List[str] = [
        dao.META_KEY, 
        rep_h.META_KEY, 
        vote.META_KEY,
        stake.META_KEY,
        proposal.META_KEY
        ] # add here new keys

    for k in keys:
        if k not in meta_data:
            meta_fill[k] = {'rows': 0}

    return meta_fill


def _get_meta_data() -> Dict:
    meta_data: Dict

    if os.path.isfile(META_PATH):
        with open(META_PATH) as json_file:
            meta_data = json.load(json_file)
    else:
        meta_data = dict() # there is not previous executions

    return _fill_empty_keys(meta_data=meta_data)


def _write_meta_data(meta: Dict) -> None:
    with open(META_PATH, 'w+') as outfile:
        json.dump(meta, outfile)
    
    print(f'Updated meta-data in {META_PATH}')


if __name__ == '__main__':
    if not os.path.isdir(DIRS):
        os.makedirs(DIRS)

    meta_data: Dict = _get_meta_data()

    # add new collectors
    collectors: List = [
        dao.update_daos, 
        rep_h.update_rep_holders,
        vote.update_votes,
        stake.update_stakes,
        proposal.update_proposals
        ]

    for c in collectors:
        c(meta_data)

    _write_meta_data(meta=meta_data)
