"""
    Descp: Metadata definitions

    Created on: 23-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from json.encoder import JSONEncoder
from typing import Dict
from pathlib import Path
import json
from datetime import datetime

import config

class Block:
    def __init__(self, init:dict=None):
        self.number = 0
        self.id = None
        self.timestamp = datetime.min

        if isinstance(init, dict):
            self.number = init["number"] if "number" in init else self.number
            self.id = init["id"] if "id" in init else self.id
            if "timestamp" in init:
                if init["timestamp"].isdigit():
                    self.timestamp = datetime.fromtimestamp(int(init["timestamp"])) if "timestamp" in init else self.timestamp
                else:
                    self.timestamp = datetime.fromisoformat(init["timestamp"])

    def __eq__(self, other):
        if isinstance(other, Block):
            # Both shouldn't be null
            return not self.id and not other.id and self.id == other.id
        else:
            return False

    def toDict(self):
        return {
            "number": self.number,
            "id": self.id,
            "timestamp": self.timestamp.isoformat()
        }

    def __str__(self):
        return self.toDict().__str__()

class NetworkMetadata:
    def __init__(self, n):
        self.block = Block()
        self._network = n

    def toDict(self):
        return {
            "block": self.block
        }

    def __eq__(self, other):
        if isinstance(other, NetworkMetadata):
            return self._network == other._network and self.block == other.block
        else:
            return False

class MetadataEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'toDict'):
            return o.toDict()
        else:
            return super().default(o)

class RunnerMetadata:
    def __init__(self, runner):
        self._path = Path('datawarehouse') / runner.name / 'metadata.json'
        self.networkMetaData: Dict[str, NetworkMetadata] = {}
        self._prev = self.networkMetaData.copy()

    def __getitem__(self, key):
        if key not in self.networkMetaData:
            self.networkMetaData[key] = NetworkMetadata(key)
        return self.networkMetaData[key]
    
    def __setitem__(self, key, val):
        self.networkMetaData[key] = val
        self.ifdump()

    def __delitem__(self, key):
        del self.networkMetaData[key]

    def load(self):
        with open(self._path, 'r') as f:
            self.networkMetadata = json.load(f)
            self._prev = self.networkMetaData.copy()

    def dump(self):
        with open(self._path, 'w') as f:
            json.dump(self.networkMetaData, f, 
                indent=2 if config.debug else None, 
                cls=MetadataEncoder)

    def ifdump(self):
        if self.networkMetaData != self._prev:
            self.dump()

    def __enter__(self):
        if self._path.is_file():
            self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.dump()
