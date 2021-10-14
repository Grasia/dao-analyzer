__args = None


def populate_args(args):
    global __args
    __args = args


def __getattr__(name):
    """
    Called when no function has been defined. Defaults to search argsparser.
    """
    return __args.__getattribute__(name)
