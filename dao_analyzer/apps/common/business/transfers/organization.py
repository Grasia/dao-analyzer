"""
   Descp: Organization transfers.

   Created on: 3-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict

from datetime import date

from dao_analyzer.apps.common.resources.strings import TEXT


class Organization:
    def __init__(self,
        o_id: str = TEXT['no_data'],
        name: str = TEXT['no_data'],
        network: str = TEXT['no_data'],
        creation_date: date = None
    ):
        self._id: str = o_id
        self._name: str = name
        self._network: str = network
        self._creation_date: date = creation_date

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

    def to_plotly_json(self) -> Dict[str, str]:
        """ Allows to store the object inside a Dcc.Store """
        return {
            'address': self.get_id(),
            'name': self.get_name(),
            'network': self.get_network(),
            'creation_date': self.get_creation_date(),
        }

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_network(self) -> str:
        return self._network

    def get_creation_date(self) -> date:
        return self._creation_date

    def get_label(self) -> str:
        if not self._name:
            return f"{self._id[:16]}... ({self._network})"
        
        return f"{self._name} ({self._id[:8]}... {self._network})"

    def get_label_long(self) -> str:
        if not self._name:
            return f"{self._id} ({self._network})"

        return f"{self._name} — {self._id} ({self._network})"

class OrganizationList(list):
    __ALL_ORGS_ID: str = '1'


    def __init__(self, orgs: List[Organization] = None) -> None:
        super().__init__(orgs)


    def add_organization(self, org: Organization) -> None:
        if org:
            self.__orgs.append(org)

    
    def get_organizations(self) -> List[Organization]:
        return list(self)

    def get_all_orgs_dict(self) -> Dict[str, str]:
        return {'value': self.__ALL_ORGS_ID, 'label': TEXT['all_orgs']}

    def get_dict_representation(self) -> List[Dict[str, str]]:
        if not self:
            return list()
        
        result: List[Dict[str, str]] = [x.get_dict_representation() for x in sorted(self)]

        # Append all_orgs as the first one
        result = [self.get_all_orgs_dict()] + result
        return result

    @classmethod
    def is_all_orgs(cls, o_id: str):
        return o_id == cls.__ALL_ORGS_ID


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
