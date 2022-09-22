"""
   Descp: This is a dao (data access object) of the platform.
    It's used to drive the data trasformation from datawarehouse to transfer obj.

   Created on: 01-jun-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""
import abc
import logging
import pandas as pd

from typing import Callable, Any

from datetime import datetime

from dao_analyzer.web.apps.common.business.singleton import ABCSingleton
from dao_analyzer.web.apps.common.business.transfers import Platform
from dao_analyzer.web.apps.common.business.transfers.organization.organization_list import OrganizationList
from dao_analyzer.web.apps.common.data_access.requesters.cache_requester import CacheRequester

# TODO: Check how caching holds in a multi-process environment (like gunicorn)
# Will there be any race conditions? It's fine if a process uses the cache generated
# by another one? What happens when the datawarehouse date changes?
# Remember that there is an inter-process cache (Flask-Caching) and an inter-thread one (CacheRequester)
# Perhaps we should create a "NonCacheRequester" which doesn't save its results in cache
def platform_memoize(f: Callable[..., Any]) -> Callable[..., Any]:
    """Use flask-caching to memoize either get_platform or get_organization_list

    When the `_requester` is updated, all meoized functions will delete is memoized
    data. This is defined at `self.delete_memoized`.

    Args:
        f (Callable): The function to wrap

    Returns:
        Callable: The wrapped function
    """

    return cache.memoize(
        timeout=3600*24,
    )(f)

class PlatformDAO(metaclass=ABCSingleton):
    def __init__(self, requester: CacheRequester):
        self._requester = requester
        self._requester._on_reload = self.delete_memoized
        self._logger = logging.getLogger(f'app.platformDAO.{self.__class__.__name__}')
        
    def delete_memoized(self, prev_date: datetime) -> None:
        if prev_date == self._requester.MIN_DATE:
            # DO NOT force clear cache if it's just initialization
            self._logger.info(f'Skipping delete memoized. prev_date: {prev_date}, new_date: {self._requester.get_last_update()}')
            return

        self._logger.debug('Requester reloaded. Deleting memoized data.')

        for d in dir(self):
            try:
                f = getattr(self, d)
                f.__func__.delete_memoized()
            except AttributeError:
                pass

    def __repr__(self):
        return f'{self.__class__.__name__}(requester={repr(self._requester)})'

    @platform_memoize
    def get_last_update_str(self) -> datetime:
        return self._requester.get_last_update_str()

    @staticmethod
    def _NaTtoNone(d) -> datetime:
        return None if pd.isna(d) else d

    @abc.abstractmethod
    def get_platform(self, orglist: OrganizationList = None) -> Platform:
        """Gets the platform

        Args:
            orglist (OrganizationList, optional): If not None, limits the organizations used to get the platform info. Defaults to None.

        Returns:
            Platform: The object with the platform information
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_organization_list(self) -> OrganizationList:
        """Gets the organization list

        Returns:
            OrganizationList: The organization list with all its attributes
        """
        raise NotImplementedError
