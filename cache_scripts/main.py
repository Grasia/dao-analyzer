#!/usr/bin/env python3
from typing import Dict, List
from aragon.runner import AragonRunner
from daohaus.runner import DaohausRunner
from daostack.runner import DaostackRunner
from common import Runner
from argparser import CacheScriptsArgParser

import config

from datetime import date
import os

import logging

LOGGING_STR_FORMAT = "%(levelname)s: %(message)s"

config.DATAWAREHOUSE.mkdir(exist_ok=True)
logging.basicConfig(format=LOGGING_STR_FORMAT, level=logging.INFO, filename=config.DATAWAREHOUSE / 'cache_scripts.log')

AVAILABLE_PLATFORMS: Dict[str, Runner] = {
    AragonRunner.name: AragonRunner(),
    DaohausRunner.name: DaohausRunner(),
    DaostackRunner.name: DaostackRunner()
}

# Get available networks from Runners
AVAILABLE_NETWORKS = {n for x in AVAILABLE_PLATFORMS.values() for n in x.networks}

def _call_platform(platform: str, force: bool=False, networks=None, collectors=None):
    AVAILABLE_PLATFORMS[platform].run(networks=networks, force=force, collectors=collectors)

if __name__ == '__main__':
    parser = CacheScriptsArgParser(
        available_platforms=list(AVAILABLE_PLATFORMS.keys()),
        available_networks=AVAILABLE_NETWORKS)

    config.populate_args(parser.parse_args())

    if config.debug:
        logging.getLogger().setLevel(level=logging.DEBUG)
    else:
        logging.getLogger().setLevel(level=logging.WARNING)

    # The default config is every platform
    if not config.platforms:
        config.platforms = AVAILABLE_PLATFORMS.keys()

    # Now calling the platform and deleting if needed
    for p in config.platforms:
        _call_platform(p, config.force, config.networks, config.collectors)

    # write date
    data_date: str = str(date.today())

    with open(os.path.join('datawarehouse', 'update_date.txt'), 'w') as f:
        f.write(data_date)
