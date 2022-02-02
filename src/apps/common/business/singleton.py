"""
   Descp: Creates a Singleton metaclass used by the app services

   Created on: 22-sep-2021

   Copyright 2021-2021 David Davó Laviña
        <david@ddavo.me>
"""
from abc import ABCMeta
import threading
import inspect

def makeHashable(o):
    if isinstance(o, tuple) or isinstance(o, set) or isinstance (o, list):
        return frozenset([makeHashable(x) for x in o])
    elif isinstance(o, dict):
        return frozenset([(k, makeHashable(v)) for k,v in o.items()])
    else:
        return o

# Extract by https://stackoverflow.com/q/6760685/4505998
# Added support for call with arguments (which return different instantiations)
class Singleton(type):
    _instances = {}
    _init = {}

    def _s_get_key(cls, args, kwargs):
        if cls in cls._init:
            return (cls, makeHashable(inspect.getcallargs(cls._init[cls], None, *args, **kwargs)))
        else:
            return cls

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._init[cls] = dict.get('__init__', None)

    def __call__(cls, *args, **kwargs):
        key = cls._s_get_key(args, kwargs)
        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]

# Extract from https://stackoverflow.com/a/51897195/4505998
class ThreadSafeSingleton(Singleton):
    __lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # Double check to avoid locking when reading
        key = cls._s_get_key(args, kwargs)
        if key not in cls._instances:
            with cls.__lock:
                return super().__call__(*args, **kwargs)

        return cls._instances[key]

# To avoid meta clashes
class ABCSingleton(Singleton, ABCMeta):
    pass

class ABCThreadSafeSingleton(ThreadSafeSingleton, ABCMeta):
    pass