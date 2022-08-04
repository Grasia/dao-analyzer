"""
   Descp: Platform transfers.

   Created on: 1-jun-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""

from typing import List, Dict, Any

from datetime import datetime

from .participation_stats import ParticipationStat

class Platform:
    def __init__(self,
        name: str,
        networks: List[str] = [],
        participation_stats: List[ParticipationStat] = [],
        creation_date: datetime = None,
    ):
        self._name = name
        self._networks = networks
        self._stats = participation_stats
        self._creation_date = creation_date

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._name.lower()

    @property
    def networks(self) -> List[str]:
        return self._networks

    @property
    def participation_stats(self) -> List[ParticipationStat]:
        return self._stats

    @property
    def creation_date(self) -> datetime:
        return self._creation_date

    def get_dropdown_representation(self) -> List[Dict[str, str]]:
        return self._orgs.get_dict_representation()

    def to_plotly_json(self) -> Dict[str, Any]:
        return {
            'name': str(self.name),
            'networks': list(self.networks),
            'stats': list(self.participation_stats),
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
        }

    @classmethod
    def from_json(cls, dict: Dict[str, Any]) -> 'Platform':
        if not dict:
            return None
        
        return Platform(
            name = dict['name'],
            networks = dict['networks'],
            participation_stats = list(map(ParticipationStat.from_json, dict.get('stats', []))),
            creation_date = None if dict['creation_date'] == 'NaT' else datetime.fromisoformat(dict['creation_date']),
        )