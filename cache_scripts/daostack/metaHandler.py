import json
import os
from typing import Dict, List


META_DATA_PATH: str = os.path.join('datawarehouse', 'daostack', 'meta_data.json')
daos: Dict = dict()

def get