"""
    Descp: Metadata definitions

    Created on: 23-nov-2021

    Copyright 2021 David Davó
        <david@ddavo.me>
"""
from json.encoder import JSONEncoder
from typing import Dict
import json
from datetime import datetime

import config

class Block:
    def __init__(self, init=None):
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

class CollectorMetaData:
    def __init__(self, c: str, d = None):
        self.block = Block()
        self._collector: str = c

        if d:
            self.block = Block(d["block"])

    def toDict(self):
        return {
            "block": self.block
        }

    def __eq__(self, other):
        if isinstance(other, CollectorMetaData):
            return self._collector == other._collector and self.block == other.block
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
        self._path = config.DATAWAREHOUSE / runner.name / 'metadata.json'
        self.collectorMetaData: Dict[str, CollectorMetaData] = {}
        self.errors: Dict[str, str] = {}
        self._setPrev()

    def _setPrev(self):
        self._prev = (self.errors.copy(), self.collectorMetaData.copy())
    
    @property
    def dirty(self) -> bool:
        return (self.errors, self.collectorMetaData) != self._prev

    def __getitem__(self, key):
        if key not in self.collectorMetaData:
            self.collectorMetaData[key] = CollectorMetaData(key)
        return self.collectorMetaData[key]
    
    def __setitem__(self, key, val):
        self.collectorMetaData[key] = val
        self.ifdump()

    def __delitem__(self, key):
        del self.collectorMetaData[key]

    def load(self):
        with open(self._path, 'r') as f:
            j = json.load(f)
            self.collectorMetaData = {k:CollectorMetaData(k,v) for k,v in j["metadata"].items()}
            self.errors = j["errors"]
            self._setPrev()

    def dump(self):
        with open(self._path, 'w') as f:
            json.dump({
                "metadata": self.collectorMetaData,
                "errors": self.errors
            }, f, 
                indent=2 if config.debug else None, 
                cls=MetadataEncoder)

    def ifdump(self):
        if self.dirty:
            self.dump()

    def __enter__(self):
        if self._path.is_file():
            self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dump()
