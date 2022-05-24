"""
   Descp: Metric adapter common interface.

   Created on: 1-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import abc
from typing import Dict

class IMetricAdapter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_plot_data') and
            callable(subclass.get_plot_data) or
            NotImplemented)


    @abc.abstractmethod
    def get_plot_data(self, dao_id: str, organizations) -> Dict:
        """
        This method it is used to transform business metrics to a dict for 
        its visual representation.
        Arguments: 
                * dao_id: The id of the dao you want to get the data.
        Return:
            A dictionary with the keys to plot it.
        """
        raise NotImplementedError
