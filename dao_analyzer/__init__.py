from . import _version

__version__ = _version.version

def create_app(test_config=None):
    from .app import server
    return server
