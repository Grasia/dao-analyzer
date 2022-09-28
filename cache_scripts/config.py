from pathlib import Path
import os

from . import __version__

CACHE_SCRIPTS_VERSION = __version__

# https://letsexchange.io/blog/what-is-block-confirmation-on-ethereum-and-how-many-confirmations-are-required/
# Number of blocks to skip to only consult confirmed blocks
SKIP_INVALID_BLOCKS = 250
DEFAULT_DATAWAREHOUSE = Path(os.getenv('DAOA_DW_PATH', 'datawarehouse'))

# LOGGING CONFIG
LOGGING_BACKUP_COUNT = os.getenv('DAOA_LOGGING_BACKUP_COUNT', 3)
LOGGING_MAX_MB = os.getenv('DAOA_LOGGING_MAX_MB', 100)

__args = None

def populate_args(args):
    global __args
    __args = args


def __getattr__(name):
    """
    Called when no function has been defined. Defaults to search argsparser.
    """
    return __args.__getattribute__(name)
