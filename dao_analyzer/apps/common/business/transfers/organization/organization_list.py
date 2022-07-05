"""
   Descp: Organization list transfers.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict, Union, Set

from .organization import Organization
from .organization_filter import Filter, NetworkFilters, SIMPLE_FILTERS, OrganizationFilterGroup

from dao_analyzer.apps.common.resources.strings import TEXT

class OrganizationList(list):
    ALL_ORGS_ID = '-1'

    def __init__(self, orgs: Union[List[Organization], List[dict]] = []) -> None:
        # Convert every item to Organization Type
        orgs = list(orgs)
        if len(orgs) > 0:
            if isinstance(orgs[0], Organization):
                super().__init__(orgs)
            else:
                super().__init__(map(Organization.from_json, orgs))

    def add_organization(self, org: Organization) -> None:
        if org:
            self.__orgs.append(org)

    def get_organizations(self) -> List[Organization]:
        return list(self)

    def get_all_orgs_dict(self) -> Dict[str, str]:
        return {'value': self.ALL_ORGS_ID, 'label': TEXT['all_orgs']}

    def get_dict_representation(self) -> List[Dict[str, str]]:
        if len(self) == 0:
            return []

        result: List[Dict[str, str]] = [x.get_dict_representation() for x in sorted(self)]

        # Append all_orgs as the first one
        result = [self.get_all_orgs_dict()] + result
        return result

    @classmethod
    def from_dict_representation(cls, dict_repr: List[Dict[str,str]]) -> 'OrganizationList':
        return OrganizationList([Organization(o['value']) for o in dict_repr])

    @classmethod
    def is_all_orgs(cls, o_id: str):
        return o_id == cls.ALL_ORGS_ID


    def is_empty(self) -> bool:
        return len(self) == 0


    def get_size(self) -> int:
        return len(self)


    def get_ids_from_id(self, o_id: str) -> List[str]:
        """
        Gets a list of ids from a o_id attr.
        If o_id is equals to 'all orgs' id then returns a list with all the orgs id.
        If not returns a list with o_id as unique element of the list.
        """
        if self.is_empty():
            return list()

        if not self.is_all_orgs(o_id):
            return [o_id]

        return [x.get_id() for x in self]

    def get_networks(self) -> Set[str]:
        return set((x.get_network().lower() for x in self))

    def get_filters(self, values=None, only_enabled=False, force_disabled=False) -> List[Filter]:
        filters = [f() for f in SIMPLE_FILTERS]

        if values is not None:
            for f in filters:
                f.enabled = f.id in values

        if force_disabled:
            for f in filters:
                f.enabled = False

        if only_enabled:
            filters = [f for f in filters if f.enabled]

        return filters

    def get_filter_group(self, *args, **kwargs) -> OrganizationFilterGroup:
        return OrganizationFilterGroup(self.get_filters(*args, **kwargs))

    def get_network_filters(self, network_values=None, only_enabled=False, force_disabled=False) -> NetworkFilters:
        nf = NetworkFilters(self.get_networks())

        if network_values is not None:
            for f in nf._filters:
                f.enabled = f.id in network_values

        if force_disabled:
            for f in nf._filters:
                f.enabled = False

        if only_enabled:
            nf._filters = [f for f in nf._filters if f.enabled]

        return nf

    def filter(self, values=None, network_values=None, **kwargs) -> 'OrganizationList':
        """ Returns a new OrganizationList with only filtered items """
        filtered = filter(self.get_filter_group(values, **kwargs).pred, self)
        filtered = filter(self.get_network_filters(network_values, **kwargs).pred, filtered)
        return OrganizationList(filtered)