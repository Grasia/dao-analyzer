"""
   Descp: Creates a Singleton metaclass used by the app services

   Created on: 22-sep-2021

   Copyright 2021-2021 David Davó Laviña
        <david@ddavo.me>
"""

# Extract by https://stackoverflow.com/q/6760685/4505998
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]