"""
   Descp: This class is used to build a unix date.

   Created on: 7-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd

class UnixDateBuilder():
    UNIX_SPACER: datetime = datetime(1970, 1, 1)

    def __init__(self):
        self._date = datetime.now()


    def set_date(self, date: datetime) -> None:
        self._date = date


    def add(self, year: int = 0, month: int = 0, day: int = 0, 
        hour: int = 0, minute: int = 0, second: int = 0):
        
        if year > 0:
            self._date = self._date + rd(years=+year)
        if month > 0:
            self._date = self._date + rd(months=+month)
        if day > 0:
            self._date = self._date + rd(days=+day)
        if hour > 0:
            self._date = self._date + rd(hours=+hour)
        if minute > 0:
            self._date = self._date + rd(minutes=+minute)
        if second > 0:
            self._date = self._date + rd(seconds=+second)
        
        return self


    def sub(self, year: int = 0, month: int = 0, day: int = 0, 
        hour: int = 0, minute: int = 0, second: int = 0) -> None:
        
        if year > 0:
            self._date = self._date + rd(years=-year)
        if month > 0:
            self._date = self._date + rd(months=-month)
        if day > 0:
            self._date = self._date + rd(days=-day)
        if hour > 0:
            self._date = self._date + rd(hours=-hour)
        if minute > 0:
            self._date = self._date + rd(minutes=-minute)
        if second > 0:
            self._date = self._date + rd(seconds=-second)

        return self


    def change(self, year: int = 0, month: int = 0, day: int = 0, 
        hour: int = -1, minute: int = -1, second: int = -1) -> None:
        
        if year > 0:
            self._date = self._date + rd(year=year)
        if month > 0:
            self._date = self._date + rd(month=month)
        if day > 0:
            self._date = self._date + rd(day=day)
        if hour >= 0:
            self._date = self._date + rd(hour=hour)
        if minute >= 0:
            self._date = self._date + rd(minute=minute)
        if second >= 0:
            self._date = self._date + rd(second=second)

        return self


    def unix(self) -> int:
        return (self._date - self.UNIX_SPACER).total_seconds()
