"""
   Descp: Flask-cache container. Avoids circular imports.

   Created on: 08-aug-2022

   Copyright 2022-2022 David Davó Laviña
        <david@ddavo.me>
"""
from typing import Dict

import os
import logging

from flask_caching import Cache

def get_cache_config(debug=False) -> Dict[str, str]:
    # Using SimpleCache by default
    cache_config = {
        'CACHE_TYPE': 'NullCache',
        'DEBUG': debug, 
        'CACHE_DEFAULT_TIMEOUT': 3600, # One hour
    }
        
    if 'DAOA_CACHE_REDIS_URL' in os.environ:
        cache_config['CACHE_TYPE'] = 'RedisCache'
        cache_config['CACHE_REDIS_URL'] = os.environ['DAOA_CACHE_REDIS_URL']
    elif 'DAOA_CACHE_DIR' in os.environ:
        cache_config['CACHE_TYPE'] = 'FileSystemCache'
        cache_config['CACHE_DIR'] = os.environ['DAOA_CACHE_DIR']
    elif not debug:
        logging.warn("""Cache not configured. Using SimpleCache by default. Setting up redis or file caching is recommended using DAOA_CACHE_DIR or DAOA_CACHE_REDIS_URL env variable.""")

    if cache_config['CACHE_TYPE'] in ['SimpleCache']:
        raise ValueError(f"CACHE_TYPE {cache_config['CACHE_TYPE']} not supported because it is not threadsafe")
    
    return cache_config

cache = Cache()
