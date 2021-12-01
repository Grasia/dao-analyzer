#!/usr/bin/env python3
from typing import Dict
from shutil import rmtree
from aragon.runner import AragonRunner
from daohaus.runner import DaohausRunner
from daostack.runner import DaostackRunner
from common import Runner
from argparser import CacheScriptsArgParser

import config

from datetime import date
from pathlib import Path

import logging

LOGGING_STR_FORMAT = "%(levelname)s: %(message)s"

AVAILABLE_PLATFORMS: Dict[str, Runner] = {
    AragonRunner.name: AragonRunner(),
    DaohausRunner.name: DaohausRunner(),
    DaostackRunner.name: DaostackRunner()
}

# Get available networks from Runners
AVAILABLE_NETWORKS = {n for x in AVAILABLE_PLATFORMS.values() for n in x.networks}

def _call_platform(platform: str, force: bool=False, networks=None, collectors=None):
    AVAILABLE_PLATFORMS[platform].run(networks=networks, force=force, collectors=collectors)

def _is_good_version(datawarehouse: Path) -> bool:
    versionfile = datawarehouse / 'version.txt'
    if not versionfile.is_file():
        return False

    with open(versionfile, 'r') as vf:
        return vf.readline().startswith(config.CACHE_SCRIPTS_VERSION)

if __name__ == '__main__':
    parser = CacheScriptsArgParser(
        available_platforms=list(AVAILABLE_PLATFORMS.keys()),
        available_networks=AVAILABLE_NETWORKS)

    config.populate_args(parser.parse_args())

    if config.datawarehouse.is_dir() and (config.delete_force or not _is_good_version(config.datawarehouse)):
        rmtree(config.datawarehouse)

    config.datawarehouse.mkdir(exist_ok=True)
    logger = logging.getLogger('cache_scripts')
    logger.addHandler(logging.FileHandler(config.datawarehouse / 'cache_scripts.log'))

    if config.debug:
        logger.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=logging.WARNING)

    # The default config is every platform
    if not config.platforms:
        config.platforms = AVAILABLE_PLATFORMS.keys()

    # Now calling the platform and deleting if needed
    for p in config.platforms:
        _call_platform(p, config.force, config.networks, config.collectors)

    # write date
    data_date: str = str(date.today().isoformat())

    if config.block_datetime:
        data_date = config.block_datetime.date().isoformat()

    with open(config.datawarehouse / 'update_date.txt', 'w') as f:
        f.write(data_date)

    with open(config.datawarehouse / 'version.txt', 'w') as f:
        f.write(config.CACHE_SCRIPTS_VERSION)
