__version__ = '0.8.2'

def create_app(test_config=None):
    from .app import server
    return server
