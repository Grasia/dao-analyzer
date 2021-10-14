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

logging.basicConfig(format=LOGGING_STR_FORMAT, level=logging.INFO)

if __name__ == '__main__':
    config.populate_args(parser.parse_args())

    if config.debug:
        logging.getLogger().setLevel(level=logging.DEBUG)

    if config.force and os.path.isdir("datawarehouse"):
        shutil.rmtree("datawarehouse")

    available_platforms = {
        "aragon": aragon.run,
        "daostack": daostack.run,
        "daohaus": daohaus.run
    }

    if not config.platforms:
        for f in available_platforms.values():
            f()

    for p in config.platforms:
        if p not in available_platforms.keys():
            print("Platform", p, "not found, available platforms are:")
            print("  ", ", ".join(available_platforms.keys()))
            exit(1)

        available_platforms[p]()

    # write date
    data_date: str = str(date.today())

    with open(os.path.join('datawarehouse', 'update_date.txt'), 'w') as f:
        f.write(data_date)
