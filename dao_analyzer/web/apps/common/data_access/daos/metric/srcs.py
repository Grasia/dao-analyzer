"""
   Descp: This file stores the common path of the datawarehouse

   Created on: 28-sep-2022

   Copyright 2022 David Davó
        <david@ddavo.me>
"""
from pathlib import Path
import os

DATAWAREHOUSE: Path = Path(os.getenv('DAOA_DW_PATH', './datawarehouse'))
