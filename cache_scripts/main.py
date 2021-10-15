#!/usr/bin/env python3
import daostack.main as daostack
import daohaus.main as daohaus
import aragon.main as aragon

import config

from datetime import date
import os
import shutil

import argparse
import logging

LOGGING_STR_FORMAT = "%(levelname)s: %(message)s"

parser = argparse.ArgumentParser(
    description="Main script to populate dao-analyzer cache")
parser.add_argument(
    "platforms",
    nargs='*',
    help="The platforms to update. Every platform is updated by default."
)
parser.add_argument(
    "--ignore-errors",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="Whether to ignore errors and continue")
parser.add_argument(
    "-d", "--debug",
    action='store_true', default=False,
    help="Shows debug info"
)
parser.add_argument(
    "-f", "--force",
    action='store_true', default=False,
    help="Removes the cache before updating"
)
parser.add_argument(
    "--skip-daohaus-names",
    action="store_true", default=False,
    help="Skips the step of getting Daohaus Moloch's names, which takes some time"
)

logging.basicConfig(format=LOGGING_STR_FORMAT, level=logging.INFO)

AVAILABLE_PLATFORMS = {
    "aragon": aragon.run,
    "daostack": daostack.run,
    "daohaus": daohaus.run
}

def _call_platform(platform: str, force: bool=False):
    platform_dir = os.path.join("datawarehouse", platform)
    print("Platform_dir", platform_dir)
    if force and os.path.isdir(platform_dir):
        logging.warning(f"Removing path {platform_dir}")
        shutil.rmtree(platform_dir)

    AVAILABLE_PLATFORMS[platform]()

if __name__ == '__main__':
    config.populate_args(parser.parse_args())

    if config.debug:
        logging.getLogger().setLevel(level=logging.DEBUG)

    # Checking whether there is an unknown platform
    for p in config.platforms:
        if p not in AVAILABLE_PLATFORMS.keys():
            print("Platform", p, "not found, available platforms are:")
            print("  ", ", ".join(AVAILABLE_PLATFORMS.keys()))
            exit(1)

    # The default config is every platform
    if not config.platforms:
        config.platforms = AVAILABLE_PLATFORMS.keys()

    # Now calling the platform and deleting if needed
    for p in config.platforms:
        _call_platform(p, config.force)

    # write date
    data_date: str = str(date.today())

    with open(os.path.join('datawarehouse', 'update_date.txt'), 'w') as f:
        f.write(data_date)
