"""
   Descp: Platform transfers.

   Created on: 1-jun-2022

   Copyright 2022 David Davó Laviña
        <ddavo@ucm.es>
"""

from typing import List, Dict, Any

from datetime import datetime

from dao_analyzer.apps.common.business.transfers.organization.organization_filter import OrganizationFilter

from .organization_list import OrganizationList
from .participation_stats import ParticipationStat

class Platform:
    def __init__(self,
        name: str,
        networks: List[str] = [],
        participation_stats: List[ParticipationStat] = [],
        organization_list: OrganizationList = OrganizationList(),
        creation_date: datetime = None,
    ):
        self._name = name
        self._networks = networks
        self._stats = participation_stats
        self._orgs = organization_list
        self._creation_date = creation_date

        if self._orgs and not self._networks:
            self._networks = list(set((x.get_network() for x in self._orgs)))

    @property
    def name(self) -> str:
        return self._name

    @property
    def networks(self) -> List[str]:
        return self._networks

    @property
    def participation_stats(self) -> List[ParticipationStat]:
        return self._stats

    @property
    def organization_list(self) -> OrganizationList:
        return self._orgs

    @property
    def creation_date(self) -> datetime:
        return self._creation_date

    def is_all_orgs(self, o_id: str) -> bool:
        return self.organization_list.is_all_orgs(o_id)

    def get_filters(self, **kwargs) -> List[OrganizationFilter]:
        return self.organization_list.get_filters(**kwargs)

    def get_dropdown_representation(self) -> List[Dict[str, str]]:
        return self._orgs.get_dict_representation()

    def get_default_org_value(self) -> str:
        return self._orgs.ALL_ORGS_ID

    def to_plotly_json(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'networks': self.networks,
            'stats': self.participation_stats,
            'orgs': self.organization_list,
            'creation_date': self.creation_date.isoformat(),
        }

    @classmethod
    def from_json(cls, dict: Dict[str, Any]) -> 'Platform':
        return Platform(
            name = dict['name'],
            networks = dict['networks'],
            participation_stats = list(map(ParticipationStat.from_json, dict.get('stats', []))),
            organization_list = OrganizationList(dict.get('orgs', [])),
            creation_date = datetime.fromisoformat(dict['creation_date']),
        )