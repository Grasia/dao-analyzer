"""
   Descp: Main script to create the DAOhaus cache, it call all the collectors.

   Created on: 29-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import json
from typing import Dict, List
from daohaus.collectors import moloch_collector as moloch
from daohaus.collectors import member_collector as member
from daohaus.collectors import vote_collector as vote
from daohaus.collectors import rage_quit_collector as rage_quit

DIRS: str = os.path.join('datawarehouse', 'daohaus')
META_PATH: str = os.path.join(DIRS, 'meta.json')


def _fill_empty_keys(meta_data: Dict) -> Dict:
    meta_fill: Dict = meta_data
    keys: List[str] = [
        moloch.META_KEY,
        member.META_KEY,
        vote.META_KEY,
        rage_quit.META_KEY,
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


def run() -> None:
    if not os.path.isdir(DIRS):
        os.makedirs(DIRS)

    meta_data: Dict = _get_meta_data()

    # add new collectors
    collectors: List = [
        moloch.update_moloches,
        member.update_members,
        vote.update_votes,
        rage_quit.update_rage_quits,
        ]

    for c in collectors:
        c(meta_data)

    _write_meta_data(meta=meta_data)


if __name__ == '__main__':
    run()
