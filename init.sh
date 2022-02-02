#!/bin/sh

cache_scripts () {
    python cache_scripts/main.py --ignore-errors $DAOA_CACHE_ARGUMENTS
}

if [ -d "datawarehouse" ]; then
    cache_scripts
else
    { sleep 60; cache_scripts; } &
fi
gunicorn index:server -c gunicorn_config.py