# https://letsexchange.io/blog/what-is-block-confirmation-on-ethereum-and-how-many-confirmations-are-required/
# Number of blocks to skip to only consult confirmed blocks
from pathlib import Path

SKIP_INVALID_BLOCKS = 250
DATAWAREHOUSE = Path('datawarehouse')

__args = None


def populate_args(args):
    global __args
    __args = args


def __getattr__(name):
    """
    Called when no function has been defined. Defaults to search argsparser.
    """
    return __args.__getattribute__(name)
