#!/bin/sh
if [ ! -d datawarehouse ]; then
    python cache_scripts/main.py --ignore-errors --skip-daohaus-names
fi

gunicorn index:server -c gunicorn_config.py