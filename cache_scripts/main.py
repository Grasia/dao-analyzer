#!/usr/bin/env python3
from parser import CacheScriptsArgParser
import daostack.main as daostack
import daohaus.main as daohaus
import aragon.main as aragon

import config

from datetime import date
import os
import shutil

import logging

LOGGING_STR_FORMAT = "%(levelname)s: %(message)s"

logging.basicConfig(format=LOGGING_STR_FORMAT, level=logging.INFO)

AVAILABLE_PLATFORMS = {
    "aragon": aragon.run,
    "daostack": daostack.run,
    "daohaus": daohaus.run
}

AVAILABLE_NETWORKS = ["mainnet", "xdai", "polygon", "arbitrum"]

def _call_platform(platform: str, force: bool=False, networks=None):
    platform_dir = os.path.join("datawarehouse", platform)
    print("Platform_dir", platform_dir)
    if force and os.path.isdir(platform_dir):
        logging.warning(f"Removing path {platform_dir}")
        shutil.rmtree(platform_dir)

    AVAILABLE_PLATFORMS[platform](networks)

if __name__ == '__main__':
    parser = CacheScriptsArgParser(
        available_platforms=list(AVAILABLE_PLATFORMS.keys()),
        available_networks=AVAILABLE_NETWORKS)

    config.populate_args(parser.parse_args())

    if config.debug:
        logging.getLogger().setLevel(level=logging.DEBUG)

    # The default config is every platform
    if not config.platforms:
        config.platforms = AVAILABLE_PLATFORMS.keys()

    # Now calling the platform and deleting if needed
    for p in config.platforms:
        _call_platform(p, config.force, config.networks)

    # write date
    data_date: str = str(date.today())

    with open(os.path.join('datawarehouse', 'update_date.txt'), 'w') as f:
        f.write(data_date)
