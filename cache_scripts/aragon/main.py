"""
   Descp: Main script to create Aragon datawarehouse, it call all the collectors.

   Created on: 15-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import json
from typing import Dict, List, Callable

import aragon.collectors.organizations as organizations
import aragon.collectors.apps as apps
import aragon.collectors.mini_me_token as token
import aragon.collectors.token_holders as holders
import aragon.collectors.repo as repos
import aragon.collectors.vote as votes
import aragon.collectors.cast as casts
import aragon.collectors.transaction as transactions

with open(os.path.join('cache_scripts', 'endpoints.json')) as json_file:
    ENDPOINTS: Dict = json.load(json_file)

DIRS: str = os.path.join('datawarehouse', 'aragon')
META_PATH: str = os.path.join(DIRS, 'meta.json')
NETWORKS: List[str] = ENDPOINTS.keys()
KEYS: List[str] = [
    organizations.META_KEY,
    apps.META_KEY,
    token.META_KEY,
    holders.META_KEY,
    repos.META_KEY,
    votes.META_KEY,
    casts.META_KEY,
    transactions.META_KEY,
] # add here new keys
COLLECTORS: List[Callable] = [
    organizations.update_organizations,
    apps.update_apps,
    token.update_tokens,
    holders.update_holders,
    repos.update_repos,
    votes.update_votes,
    casts.update_casts,
    transactions.update_transactions,
] # add new collectors


def _fill_empty_keys() -> Dict:
    meta_fill: Dict = {}

    for n in NETWORKS:
        meta_fill[n] = {}
        for k in KEYS:
            meta_fill[n][k] = {'rows': 0}

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


def run() -> None:
    print('------------- Updating Aragon\'s datawarehouse -------------\n')
    if not os.path.isdir(DIRS):
        os.makedirs(DIRS)

    meta_data: Dict = _get_meta_data()

    for n in NETWORKS:
        print(f'------------- Getting data from {n} -------------\n')
        for c in COLLECTORS:
            c(  meta_data=meta_data,
                net=n,
                endpoints=ENDPOINTS)

    _write_meta_data(meta=meta_data)
    print('------------- Aragon\'s datawarehouse updated -------------\n')


if __name__ == '__main__':
    run()
