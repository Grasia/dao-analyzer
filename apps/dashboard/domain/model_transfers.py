"""
   Descp: This file is used to store all the transfer classes.

   Created on: 26-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List
from pandas import Timestamp
from apps.dashboard.strings import TEXT

class Organization():
    def __init__(self, o_id:str = TEXT['no_data'], name:str = TEXT['no_data']):
        self.id: str   = o_id
        self.name: str = name 


class OrganizationUser():
    def __init__(self, created_at: Timestamp = Timestamp(0)):
        self.created_at: Timestamp = created_at


class MetricNewUsers():
    """
    * x = a list with timestamps month over month since first user 
          registered to today's date.
    * y = a list with new users in a 'x' month.
    * last_month_n_users = the number of users in the last month.
    * last_month_name = last month's name.
    * month_over_month = a percentage of how many users has joined among
                         the last two months.
    """
    def __init__(self, x: List[Timestamp] = list(), y: List[int] = list(), 
        last_month_n_users: int = 0, last_month_name: str = TEXT['no_data'],
        month_over_month: float = 0.0):

        self.x: List[Timestamp] = x
        self.y: List[int] = y
        self.last_month_n_users: int = y[-1] if y else last_month_n_users
        self.last_month_name: str = x[-1].strftime('%B') if x \
            else last_month_name
        self.month_over_month: float = self.__calculate_m_o_m() if y \
            else month_over_month

    def __calculate_m_o_m(self) -> float:
        val = 0.0
        # indexes to access n-1 and n-2 positions in y[n] 
        i_1 = -1
        i_2 = -(2 % (len(self.y) + 1))

        divider: int = self.y[i_1] + self.y[i_2]
        if divider > 0:
            val = (self.y[i_1] - self.y[i_2]) / divider * 100

        return val