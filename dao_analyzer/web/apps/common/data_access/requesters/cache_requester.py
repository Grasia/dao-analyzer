from typing import List
import pandas as pd
from pathlib import Path
import portalocker as pl
from datetime import datetime, timedelta, timezone
import json
import logging

from dao_analyzer.web.apps.common.business.singleton import ABCSingleton
from dao_analyzer.web.apps.common.data_access.requesters.irequester import IRequester
from dao_analyzer.web.apps.common.data_access.daos.metric.srcs import DATAWAREHOUSE

LOCK_PATH = DATAWAREHOUSE / '.lock'

class CacheRequester(IRequester, metaclass=ABCSingleton):
    CHECKING_COOLDOWN = 60

    def __init__(self, srcs: List[Path]):
        """
        Initializes the CacheRequester

            Parameters:
                srcs (List[Path]): A list of paths to read the dataframes from
        """
        self._srcs = srcs
        self._df: pd.DataFrame = pd.DataFrame()

        # Avoids having to lock the file and open the metadata with every request
        self._next_check = datetime.min

        # Lets us read the data only when necessary
        self._last_update = datetime.min.replace(tzinfo=timezone.utc)
        self.logger = logging.getLogger("app.cacherequester")

    def get_last_update(self) -> datetime:
        return self._last_update
    
    def get_last_update_str(self) -> str:
        return self.get_last_update().strftime('%b %-d, %Y at %H:%M %Z')

    def metadataTime(self) -> datetime:
        """
        Returns the latest time the dataframes have been updated
        """
        t = datetime.min.replace(tzinfo=timezone.utc)
        metadata = json.loads((self._srcs[0].parent / 'metadata.json').read_bytes())["metadata"]

        for src in self._srcs:
            collector_name = str(src.stem)
            for k,v in metadata.items():
                # Format is <platform>/<collector>-<network>
                if k.split('/')[1].split('-')[0] == collector_name:
                    t = max(t, datetime.fromisoformat(v["block"]["timestamp"]))

        return t

    def tryReload(self):
        self._df = pd.concat(map(pd.read_feather, self._srcs), axis=0, ignore_index=True)

    # https://stackoverflow.com/questions/70861731/how-to-filelock-an-entire-directory
    def request(self) -> pd.DataFrame:
        """
        Gets data from datawarehouse.
        Arguments:
            * args: Its not used
        Return:
            a pandas dataframe with all the data loaded. If the src does not 
            exist, it will return an empty dataframe.
        """
        # Whether we should check (locking can be costly)
        if self._srcs and (self._df.empty or datetime.now() > self._next_check):
            self._next_check = datetime.now() + timedelta(seconds=self.CHECKING_COOLDOWN)

            # Try checking if something has changed
            try:
                # Lock the datawarehouse as reader, and then check if the metadata changed
                with pl.Lock(LOCK_PATH, 'rb', flags=pl.LockFlags.SHARED  | pl.LockFlags.NON_BLOCKING, timeout=0.1):
                    t = self.metadataTime()
                    if t > self._last_update or self._df.empty:
                        self._last_update = t
                        self.tryReload()
            except (pl.LockException, pl.AlreadyLocked):
                self.logger.debug("Couldn't acquire lock")

        if self._df.empty:
            self.logger.warning(f"Returning empty dataframe for sources {[str(x) for x in self._srcs]}")

        return self._df
