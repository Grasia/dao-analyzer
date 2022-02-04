from pathlib import Path

CACHE_SCRIPTS_VERSION = "1.0.2"

# https://letsexchange.io/blog/what-is-block-confirmation-on-ethereum-and-how-many-confirmations-are-required/
# Number of blocks to skip to only consult confirmed blocks
SKIP_INVALID_BLOCKS = 0
DEFAULT_DATAWAREHOUSE = Path('datawarehouse')

__args = None

def populate_args(args):
    global __args
    __args = args


def __getattr__(name):
    """
    Called when no function has been defined. Defaults to search argsparser.
    """
    return __args.__getattribute__(name)
