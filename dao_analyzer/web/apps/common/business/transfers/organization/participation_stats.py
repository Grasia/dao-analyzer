"""
   Descp: Participation stats DTO.

   Created on: 31-may-2022

   Copyright 2022-2022 David Davó Laviña
        <david@ddavo.me>
"""
from typing import Dict, List, Any

import abc

from dao_analyzer.web.apps.common.resources.strings import TEXT

class ParticipationStat(metaclass=abc.ABCMeta):
    def __init__(self, value):
        self._value = value

    def to_plotly_json(self) -> Dict[str, Any]:
        """ Allows the object to be stored inside a Dcc.Store """
        return {
            'value': self._value,
            'stat': _get_stat_idx(type(self))
        }
    
    @classmethod
    def from_json(cls, d: Dict[str,Any]) -> 'ParticipationStat':
        # 1. Get the class
        statbuilder = STATS_LIST[d['stat']]

        # 2. Instantiate and return
        return statbuilder(d['value'])
    
    @property
    def value(self):
        return self._value

    @property
    def value_str(self):
        if not self.value:
            return None

        if self.value < 0.01:
            return f'{self.value*100:.2g}%'
        return f'{self.value*100:.0f}%'

    @property
    @abc.abstractmethod
    def text(self) -> str:
        raise NotImplementedError

    @classmethod
    @property
    def idx(cls) -> str:
        return str(_get_stat_idx(cls))

    @property
    def key(self) -> str:
        return f'{_get_stat_idx(self)}-{self._value}'

class MembersCreatedProposalsStat(ParticipationStat):

    @property
    def text(self) -> str:
        if self.value is None:
            return TEXT['stat_members_created_proposals_novalue']
        return TEXT['stat_members_created_proposals']

class MembersEverVotedStat(ParticipationStat):

    @property
    def text(self):
        if self.value is None:
            return TEXT['stat_members_ever_voted_novalue']
        return TEXT['stat_members_ever_voted']

STATS_LIST: List = [
    MembersCreatedProposalsStat,
    MembersEverVotedStat,
]

"""
Given an stat class, returns its index in STATS_LIST
"""
def _get_stat_idx(stat):
    return next((i for i,x in enumerate(STATS_LIST) if x == stat), None)