from argparse import ArgumentParser, BooleanOptionalAction
from typing import List

from datetime import datetime
import pathlib

import config

class CacheScriptsArgParser(ArgumentParser):
    def __init__(self, available_platforms: List[str], available_networks: List[str]):
        super().__init__(description="Main script to populate dao-analyzer cache")

        self.add_argument(
            "-p", "--platforms",
            choices=available_platforms,
            nargs='*',
            type=str,
            default=available_platforms,
            help="The platforms to update. Every platform is updated by default."
        )
        self.add_argument(
            "--ignore-errors",
            default=True,
            action=BooleanOptionalAction,
            help="Whether to ignore errors and continue")
        self.add_argument(
            "-d", "--debug",
            action='store_true', default=False,
            help="Shows debug info"
        )
        self.add_argument(
            "-f", "--force",
            action='store_true', default=False,
            help="Removes the cache before updating"
        )
        self.add_argument(
            "-F", "--delete-force",
            action="store_true", default=False,
            help="Removes the datawarehouse folder before doing anything"
        )
        self.add_argument(
            "--skip-daohaus-names",
            action="store_true", default=False,
            help="Skips the step of getting Daohaus Moloch's names, which takes some time"
        )
        self.add_argument(
            "-n", "--networks",
            nargs="+",
            required=False,
            choices=available_networks,
            default=available_networks,
            help="Networks to update. Every network is updated by default"
        )
        self.add_argument(
            "-c", "--collectors",
            nargs="+",
            required=False,
            help="Collectors to run. For example: aragon/casts"
        )
        self.add_argument(
            "--block-datetime",
            required=False,
            type=datetime.fromisoformat,
            help="Get data up to a block datetime (input in ISO format)"
        )
        self.add_argument(
            "-D", "--datawarehouse",
            help="Specifies the destination folder of the datawarehouse",
            required=False,
            type=pathlib.Path,
            default=config.DEFAULT_DATAWAREHOUSE
        )