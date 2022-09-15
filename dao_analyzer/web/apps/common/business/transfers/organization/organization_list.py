"""
   Descp: Organization list transfers.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List, Dict, Union, Set

from .organization import Organization
from .organization_filter import Filter, NetworkFilters, SIMPLE_FILTERS, NetworkRadioButton, OrganizationFilterGroup

from dao_analyzer.web.apps.common.resources.strings import TEXT

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
    
    @staticmethod
    def from_json(list: list) -> 'OrganizationList':
        return OrganizationList([] if list is None else list)

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

    @staticmethod
    def get_filters(
        values: List[str] = None,
        only_enabled: bool = False,
        force_disabled: bool = False,
        diff: bool = False
    ) -> List[Filter]:
        """Gets the filters available for an OrganizationList

        Args:
            values (List[str], optional): The ids of the filters to set to enable, if None returns default values. Defaults to None.
            only_enabled (bool, optional): When True, returns only the enabled filters. Defaults to False.
            force_disabled (bool, optional): When True, forces all filters to the disabled state. Defaults to False.
            diff (bool, optional): When True, values is the ids of the filters to change to the non-default value (see :func:`~OrganizationList.get_diff_filters`). Defaults to False.

        Returns:
            List[Filter]: The list of selected filters.
        """
        filters = [f() for f in SIMPLE_FILTERS]

        if values is not None:
            for f in filters:
                if not diff:
                    f.enabled = f.id in values
                elif diff and f.id in values:
                    f.enabled = not f.default

        if force_disabled:
            for f in filters:
                f.enabled = False

        if only_enabled:
            filters = [f for f in filters if f.enabled]

        return filters
    
    @staticmethod
    def get_diff_filters(values=None):
        """ Return filters which the value is different from the default """
        return [f for f in OrganizationList.get_filters(values) if f.enabled != f.default]

    @staticmethod
    def get_filter_group(*args, **kwargs) -> OrganizationFilterGroup:
        return OrganizationFilterGroup(OrganizationList.get_filters(*args, **kwargs))

    @staticmethod
    def get_network_filters_for(networks, network_values=None, only_enabled=False, force_disabled=False) -> NetworkFilters:
        nf = NetworkFilters(networks)

        if network_values is not None:
            for f in nf._filters:
                f.enabled = f.id in network_values

        if force_disabled:
            for f in nf._filters:
                f.enabled = False

        if only_enabled:
            nf._filters = [f for f in nf._filters if f.enabled]

        return nf
    
    def get_network_radio(self, network_value=None, **kwargs) -> NetworkRadioButton:
        return NetworkRadioButton(self.get_networks(), network_value)
    
    def get_network_filters(self, network_values=None, only_enabled=False, force_disabled=False) -> NetworkFilters:
        return self.get_network_filters_for(self.get_networks(), network_values=network_values, only_enabled=only_enabled, force_disabled=force_disabled)

    def filter(self, values=None, network_value=None, **kwargs) -> 'OrganizationList':
        """ Returns a new OrganizationList with only filtered items """
        filtered = filter(self.get_filter_group(values, **kwargs).pred, self)
        filtered = filter(self.get_network_radio(network_value, **kwargs).pred, filtered)
        return OrganizationList(filtered)