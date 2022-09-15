try:
    from . import _version

    __version__ = _version.version
except ImportError:
    __version__ = 'Unknown'

def create_app(test_config=None):
    from .app import server
    return server
