#!/bin/sh
python cache_scripts/main.py --ignore-errors $DAOA_CACHE_ARGUMENTS
gunicorn index:server -c gunicorn_config.py