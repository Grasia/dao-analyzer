"""
   Descp: Main script to create the DAOhaus cache, it call all the collectors.

   Created on: 29-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import json
import logging
from typing import Dict, List
from daohaus.collectors import moloch_collector as moloch
from daohaus.collectors import member_collector as member
from daohaus.collectors import vote_collector as vote
from daohaus.collectors import rage_quit_collector as rage_quit
from daohaus.collectors import proposal_collector as proposal

with open(os.path.join('cache_scripts', 'endpoints.json')) as json_file:
    ENDPOINTS: Dict = json.load(json_file)

DIRS: str = os.path.join('datawarehouse', 'daohaus')
META_PATH: str = os.path.join(DIRS, 'meta.json')
NETWORKS: List[str] = {n for n, v in ENDPOINTS.items() if 'daohaus' in v}
KEYS: List[str] = [
    moloch.META_KEY,
    member.META_KEY,
    vote.META_KEY,
    rage_quit.META_KEY,
    proposal.META_KEY,
] # add here new keys
COLLECTORS: List = [
    moloch.update_moloches,
    member.update_members,
    vote.update_votes,
    rage_quit.update_rage_quits,
    proposal.update_proposals,
] # add new collectors


def _fill_empty_keys() -> Dict:
    meta_fill: Dict = {}

    for n in NETWORKS:
        meta_fill[n] = {}
        for k in KEYS:
            meta_fill[n][k] = {'rows': 0, 'last_id': ""}

    return meta_fill


def _get_meta_data() -> Dict:
    meta_data: Dict

    if os.path.isfile(META_PATH):
        with open(META_PATH) as json_file:
            meta_data = json.load(json_file)
    else:
        meta_data = _fill_empty_keys()

    return meta_data


def _write_meta_data(meta: Dict) -> None:
    with open(META_PATH, 'w+') as outfile:
        json.dump(meta, outfile)
    
    print(f'Updated meta-data in {META_PATH}')


def run(do_networks=NETWORKS) -> None:
    print('------------- Updating DAOhaus\'s datawarehouse -------------\n')
    if not os.path.isdir(DIRS):
        os.makedirs(DIRS)

    meta_data: Dict = _get_meta_data()

    if not NETWORKS.intersection(do_networks):
        logging.warning(f"Network(s) {','.join(do_networks)} not found")

    for n in NETWORKS.intersection(do_networks):
        print(f'------------- Getting data from {n} -------------\n')
        for c in COLLECTORS:
            c(  meta_data=meta_data,
                net=n,
                endpoints=ENDPOINTS)

    _write_meta_data(meta=meta_data)
    print('------------- DAOhaus\'s datawarehouse updated -------------\n')


if __name__ == '__main__':
    run()
