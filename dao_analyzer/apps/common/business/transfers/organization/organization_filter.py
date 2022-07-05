
"""
   Descp: Organization list transfer filters.

   Created on: 24-may-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""

import abc
from typing import List, Callable, Iterable, Dict
from datetime import datetime, timedelta

from dao_analyzer.apps.common.business.transfers.organization.organization import Organization

from dao_analyzer.apps.common.resources.strings import TEXT

class Filter(metaclass=abc.ABCMeta):

    def pred(self, org: Organization) -> bool:
        raise NotImplementedError

class OrganizationFilter(Filter, metaclass=abc.ABCMeta):

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

class NetworkFilter(OrganizationFilter):
    def __init__(self, network: str):
        super().__init__(network, network.capitalize(), True)
        self._network = network

    def pred(self, org: Organization) -> bool:
        """
        Wether the organization is from the selected network
        """
        return org.get_network().lower() == self._network.lower()

class OrganizationFilterGroup(Filter):
    def __init__(self, filters: Iterable[OrganizationFilter] = []):
        self._filters = list(filters)

    def append(self, filter: OrganizationFilter):
        if not isinstance(filter, OrganizationFilter):
            raise TypeError

        self._filters.append(filter)

    def pred(self, org: Organization) -> bool:
        # For an item to be selected, it has to verify every filter
        return all(map(lambda f:f.pred(org), self._filters))

    def get_options(self) -> Dict[str, str]:
        return { x.id:x.title for x in self._filters }
    
    def get_value(self) -> List[str]:
        return [ x.id for x in self._filters if x.enabled ]

class NetworkFilters(OrganizationFilterGroup):
    """ A list of organization filters with an or predicate """

    def __init__(self, networks: List[str]):
        assert(networks) #  Networks can't be null nor empty
        super().__init__(map(NetworkFilter, networks))

    def pred(self, org: Organization) -> bool:
        # An item has to be in any of the selected networks
        return any(map(lambda f:f.pred(org), self._filters))

SIMPLE_FILTERS: List[Callable[[], OrganizationFilter]] = [
    ActiveLastYearFilter
]
