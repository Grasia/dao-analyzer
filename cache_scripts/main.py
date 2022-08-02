#!/usr/bin/env python3
from typing import Dict

from datetime import date
from pathlib import Path
import portalocker as pl
import os
import tempfile
import shutil
from sys import stderr

import logging
from logging.handlers import RotatingFileHandler

from .aragon.runner import AragonRunner
from .daohaus.runner import DaohausRunner
from .daostack.runner import DaostackRunner
from .common import Runner, ENDPOINTS
from .argparser import CacheScriptsArgParser
from . import config

LOG_FILE_FORMAT = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"
LOG_STREAM_FORMAT = "%(levelname)s: %(message)s"

AVAILABLE_PLATFORMS: Dict[str, Runner] = {
    AragonRunner.name: AragonRunner,
    DaohausRunner.name: DaohausRunner,
    DaostackRunner.name: DaostackRunner
}

# Get available networks from Runners
AVAILABLE_NETWORKS = {n for n in ENDPOINTS.keys() if not n.startswith('_')}

def _call_platform(platform: str, datawarehouse: Path, force: bool=False, networks=None, collectors=None):
    p = AVAILABLE_PLATFORMS[platform]()
    p.set_dw(datawarehouse)
    p.run(networks=networks, force=force, collectors=collectors)

def _is_good_version(datawarehouse: Path) -> bool:
    versionfile = datawarehouse / 'version.txt'
    if not versionfile.is_file():
        return False

    with open(versionfile, 'r') as vf:
        return vf.readline().startswith(config.CACHE_SCRIPTS_VERSION)

def main_aux(datawarehouse: Path):
    if config.delete_force or not _is_good_version(datawarehouse):
        # We skip the dotfiles like .lock
        for p in datawarehouse.glob('[!.]*'):
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

    logger = logging.getLogger()
    logger.propagate = True
    filehandler = RotatingFileHandler(
        filename=config.datawarehouse / 'cache_scripts.log',
        maxBytes=config.LOGGING_MAX_MB * 2**20,
        backupCount=config.LOGGING_BACKUP_COUNT,
    )

    filehandler.setFormatter(logging.Formatter(LOG_FILE_FORMAT))
    logger.addHandler(filehandler)
    logger.setLevel(level=logging.DEBUG if config.debug else logging.INFO)

    # Log errors to STDERR
    streamhandler = logging.StreamHandler(stderr)
    streamhandler.setLevel(logging.WARNING if config.debug else logging.ERROR)
    streamhandler.setFormatter(logging.Formatter(LOG_STREAM_FORMAT))
    logger.addHandler(streamhandler)

    # The default config is every platform
    if not config.platforms:
        config.platforms = AVAILABLE_PLATFORMS.keys()

    # Now calling the platform and deleting if needed
    for p in config.platforms:
        _call_platform(p, datawarehouse, config.force, config.networks, config.collectors)

    # write date
    data_date: str = str(date.today().isoformat())

    if config.block_datetime:
        data_date = config.block_datetime.date().isoformat()

    with open(datawarehouse / 'update_date.txt', 'w') as f:
        f.write(data_date)

    with open(datawarehouse / 'version.txt', 'w') as f:
        f.write(config.CACHE_SCRIPTS_VERSION)

def main_lock(datawarehouse: Path):
    datawarehouse.mkdir(exist_ok=True)
    
    # Lock for the datawarehouse (also used by the dash)
    p_lock: Path = datawarehouse / '.lock'

    # Exclusive lock for the chache-scripts (no two cache-scripts running)
    cs_lock: Path = datawarehouse / '.cs.lock'

    try:
        with pl.Lock(cs_lock, 'w', timeout=1) as lock, \
             tempfile.TemporaryDirectory(prefix="datawarehouse_") as tmp_dw:

            # Writing pid and dir name to lock (debugging)
            tmp_dw = Path(tmp_dw)
            print(os.getpid(), file=lock)
            print(tmp_dw, file=lock)
            lock.flush()

            ignore = shutil.ignore_patterns('*.log', '.lock*')

            # We want to copy the dw, so we open it as readers
            p_lock.touch(exist_ok=True)
            with pl.Lock(p_lock, 'r', timeout=1, flags=pl.LOCK_SH | pl.LOCK_NB):
                shutil.copytree(datawarehouse, tmp_dw, dirs_exist_ok=True, ignore=ignore)

            main_aux(datawarehouse=tmp_dw)

            with pl.Lock(p_lock, 'w', timeout=10):
                shutil.copytree(tmp_dw, datawarehouse, dirs_exist_ok=True, ignore=ignore)

            # Removing pid from lock
            lock.truncate(0)
    except pl.LockException:
        with open(cs_lock, 'r') as f:
            pid = int(f.readline())

        print(f"The cache_scripts are already being run with pid {pid}", file=stderr)
        exit(1)

def main():
    parser = CacheScriptsArgParser(
        available_platforms=list(AVAILABLE_PLATFORMS.keys()),
        available_networks=AVAILABLE_NETWORKS)

    config.populate_args(parser.parse_args())

    if config.display_version:
        print(config.CACHE_SCRIPTS_VERSION)
        exit(0)

    main_lock(config.datawarehouse)

if __name__ == '__main__':
    main()