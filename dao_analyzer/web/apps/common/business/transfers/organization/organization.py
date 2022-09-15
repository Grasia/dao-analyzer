"""
   Descp: Organization transfers.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Any

from datetime import datetime
from .participation_stats import ParticipationStat

from dao_analyzer.web.apps.common.resources.strings import TEXT

class Organization:
    def __init__(self,
        o_id: str = TEXT['no_data'],
        name: str = TEXT['no_data'],
        network: str = TEXT['no_data'],
        creation_date: datetime = None,
        first_activity: datetime = None,
        last_activity: datetime = None,
        participation_stats: List[ParticipationStat] = [],
    ):
        self._id: str = o_id
        self._name: str = name
        self._network: str = network
        self._creation_date: datetime = creation_date
        self._first_activity: datetime = first_activity
        self._last_activity: datetime = last_activity
        self._participation_stats: List[ParticipationStat] = participation_stats

    # Redefinition of sorting functions
    def __eq__(self, other) -> bool:
        return self._id == other._id and self._network == other._network

    """ First we have the items with a name sorted by name. Then the ones without
        name sorted by id
    """
    def __lt__(self, other) -> bool:
        # If self doesn't have a name, we check if other has a name
        if self._name is None:
            if other._name is None:
                return self._id < other._id
            else:
                return False

        # If self has a name, but other does not have a name,
        # then self is lower than the other
        if other._name is None:
            return True
        
        # If the name is the same, we sort by network, then by id
        if self._name.casefold() == other._name.casefold():
            if self._network.casefold() == other._network.casefold():
                return self._id < other._id
            else:
                return self._network.casefold() < other._network.casefold()
        else:
            return self._name.casefold() < other._name.casefold()
    
    def get_dict_representation(self) -> Dict[str, str]:
        return {
            'value': self._id, 
            'label': self.get_label()
        }

    def to_plotly_json(self) -> Dict[str, Any]:
        """ Allows to store the object inside a Dcc.Store """
        return {
            'address': self.get_id(),
            'name': self.get_name(),
            'network': self.get_network(),
            'creation_date': self.get_creation_date(),
            'first_activity': self.get_first_activity(),
            'last_activity': self.get_last_activity(),
            'participation_stats': self.get_participation_stats(),
        }

    @classmethod
    def from_json(cls, dict: Dict[str, Any]) -> 'Organization':
        def _getdt(key):
            d = dict.get(key, None)

            if not d:
                return None
            elif isinstance(d, str):
                return datetime.fromisoformat(d)
            else:
                raise TypeError

        participation = [ParticipationStat.from_json(x) for x in dict.get('participation_stats', [])]

        return Organization(
            o_id = dict['address'],
            network = dict['network'],
            name = dict.get('name', None),
            creation_date = _getdt('creation_date'),
            first_activity = _getdt('first_activity'),
            last_activity = _getdt('last_activity'),
            participation_stats = participation,
        )

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_network(self) -> str:
        return self._network

    def get_creation_date(self) -> datetime:
        return self._creation_date

    def get_first_activity(self) -> datetime:
        return self._first_activity

    def get_participation_stats(self) -> List[ParticipationStat]:
        return self._participation_stats

    def get_last_activity(self) -> datetime:
        return self._last_activity

    def get_label(self) -> str:
        if not self._name:
            return f"{self._id[:16]}... ({self._network})"
        
        return f"{self._name} ({self._id[:8]}... {self._network})"

    def get_label_long(self) -> str:
        if not self._name:
            return f"{self._id} ({self._network})"

        return f"{self._name} — {self._id} ({self._network})"
