"""
   Descp: Interface for requesters.

   Created on: 16-jul-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Any

class IRequester(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'request') and
            callable(subclass.request) or
            NotImplemented)


    @abc.abstractmethod
    def request(self, *args) -> Any:
        """
        Common function to request data.
        Arguments: 
                * args: a list of arguments to request
        Return:
            The return value is tied to the interface implementation. 
        """
        raise NotImplementedError
