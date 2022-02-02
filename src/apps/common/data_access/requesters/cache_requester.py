from typing import List
import pandas as pd
from pathlib import Path
import portalocker as pl
from datetime import datetime, timedelta
import json
import logging

from src.apps.common.business.singleton import ABCSingleton
from src.apps.common.data_access.requesters.irequester import IRequester

LOCK_PATH = Path('datawarehouse/.lock')

class CacheRequester(IRequester, metaclass=ABCSingleton):
    CHECKING_COOLDOWN = 60

    def __init__(self, srcs: List[Path]):
        self.__srcs = srcs
        self.__df: pd.DataFrame = pd.DataFrame()

        # Avoids having to lock the file and open the metadata with every request
        self.__next_check = datetime.min

        # Lets us read the data only when necessary
        self.__last_update = datetime.min
        self.logger = logging.getLogger("app.cacherequester")


    def metadataTime(self) -> datetime:
        """
        Returns the latest time the dataframes have been updated
        """
        t = datetime.min
        metadata = json.loads((self.__srcs[0].parent / 'metadata.json').read_bytes())["metadata"]

        for src in self.__srcs:
            collector_name = str(src.stem)
            for k,v in metadata.items():
                # Format is <platform>/<collector>-<network>
                if k.split('/')[1].split('-')[0] == collector_name:
                    t = max(t, datetime.fromisoformat(v["block"]["timestamp"]))

        return t

    def tryReload(self):
        df = pd.DataFrame()
        for src in self.__srcs:
            df = pd.concat([df, pd.read_feather(src)], axis=0, ignore_index=True)

        self.__df = df

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
        if self.__srcs and (self.__df.empty or datetime.now() > self.__next_check):
            self.__next_check = datetime.now() + timedelta(seconds=self.CHECKING_COOLDOWN)

            # Try checking if something has changed
            try:
                # Lock the datawarehouse as reader, and then check if the metadata changed
                with pl.Lock(LOCK_PATH, 'rb', flags=pl.LockFlags.SHARED  | pl.LockFlags.NON_BLOCKING, timeout=0.1):
                    t = self.metadataTime()
                    if t > self.__last_update or self.__df.empty:
                        self.__last_update = t
                        self.tryReload()
            except (pl.LockException, pl.AlreadyLocked):
                self.logger.debug("Couldn't acquire lock")

        if self.__df.empty:
            self.logger.warning(f"Returning empty dataframe for sources {[str(x) for x in self.__srcs]}")

        return self.__df
