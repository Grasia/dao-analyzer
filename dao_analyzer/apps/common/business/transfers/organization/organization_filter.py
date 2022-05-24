
"""
   Descp: Organization list transfer filters.

   Created on: 24-may-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""

import abc
from typing import List, Callable
from datetime import datetime, timedelta

from dao_analyzer.apps.common.business.transfers.organization.organization import Organization

from dao_analyzer.apps.common.resources.strings import TEXT

class OrganizationFilter(metaclass=abc.ABCMeta):

    def __init__(self, id, title, enabled):
        self._id = id
        self._title = title
        self._enabled = enabled

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = bool(value)

    @abc.abstractmethod
    def pred(self, org: Organization) -> bool:
        raise NotImplementedError


class ActiveLastYearFilter(OrganizationFilter):
    def __init__(self):
        super().__init__('active-last-year', TEXT['filter_active_last_year_title'], True)

    def pred(self, org: Organization) -> bool:
        """
        Wether the organization has been active in the last year
        """
        la = org.get_last_activity()

        # If la is defined and last activity in the last 365 days
        return la and la >= (datetime.now() - timedelta(days=365))

ALL_FILTERS: List[Callable[[], OrganizationFilter]] = [
    ActiveLastYearFilter
]
