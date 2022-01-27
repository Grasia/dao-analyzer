from typing import List
import pandas as pd
from pathlib import Path
import portalocker as pl
from datetime import datetime, timedelta
import json

from src.apps.common.data_access.requesters.irequester import IRequester

LOCK_PATH = Path('datawarehouse/.lock')

# TODO: Remove printfs
class CacheRequester(IRequester):
    CHECKING_COOLDOWN = 60

    def __init__(self, srcs: List[Path]):
        self.__srcs = srcs
        self.__df: pd.DataFrame = pd.DataFrame()

        # Avoids having to lock the file and open the metadata with every request
        self.__next_check = datetime.min

        # Lets us read the data only when necessary
        self.__last_update = datetime.min

    def metadataTime(self) -> datetime:
        """
        Returns the latest time the dataframes have been updated
        """
        t = datetime.min
        metadata = json.loads((self.__srcs[0].parent / 'metadata.json').read_bytes())["metadata"]

        # print(f"> metadata: {metadata}")
        for src in self.__srcs:
            collector_name = str(src.stem)
            for k,v in metadata.items():
                print(f"> collector_name: {collector_name}, k: {k}")
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

        if self.__srcs and (self.__df.empty or datetime.now() > self.__next_check):
            self.__next_check = datetime.now() + timedelta(seconds=self.CHECKING_COOLDOWN)
            print(f"> Checking if we should update. Next check at {self.__next_check}, in {(self.__next_check - datetime.now()).seconds} seconds")

            try:
                # TODO: Solve timeout not working with SHARED flag https://github.com/WoLpH/portalocker/issues/74
                with pl.Lock(LOCK_PATH, 'rb', flags=pl.LockFlags.SHARED, fail_when_locked=True):
                    t = self.metadataTime()
                    if t > self.__last_update:
                        print(f"> Updating now {self.__srcs}")
                        self.__last_update = t
                        self.tryReload()
                    else:
                        print(f"> Not updating yet. t: {t}, last_update: {self.__last_update}")
            except pl.AlreadyLocked:
                print("> Lock not acquired")
        elif datetime.now() <= self.__next_check:
            print(f"> Not updating yet. Next check at {self.__next_check}, in {(self.__next_check - datetime.now()).seconds} seconds")

        if (self.__df.empty): print(">>> WARNING: RETURNING EMPTY DATAFRAME!!!")

        return self.__df
