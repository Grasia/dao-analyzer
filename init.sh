#!/bin/sh

cache_scripts () {
    daoa-cache-scripts --ignore-errors $DAOA_CACHE_ARGUMENTS
}

if [ ! -f "datawarehouse/update_date.txt" ]; then
    cache_scripts
fi

gunicorn -c gunicorn_config.py
