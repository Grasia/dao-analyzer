"""
   Descp: This is used to get the last update date

   Created on: 14-april-2021

   Copyright 2021-2022 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
import os

class UpdateDate:

    def get_date(self) -> str:
        date: str

        with open(os.path.join('datawarehouse', 'update_date.txt'),'r') as f:
            date = f.readline()
        
        return date
