"""
   Descp: Tabular data transfer for use in datatables

   Created on: 16-mar-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from __future__ import annotations
from typing import Dict

import pandas as pd

class TabularData():
    def __init__(self):
        self.columns = []
        self.data = []

    @staticmethod
    def from_df(df: pd.DataFrame) -> TabularData:
        df = df.reset_index()
        self = TabularData()
        self.columns = [{"name": c, "id": c} for c in df.columns]
        self.data = df.to_dict('records')
        return self
    
    def set_column_names(self, newc: Dict[str, str]) -> TabularData:
        """Sets the column names given the id

        Args:
            newc (Dict[str, str]): A dict of id:'Column Name'
        """
        self.columns = [{'name': newc[c['id']] if c['id'] in newc else c['name'], 'id': c['id']} for c in self.columns]
        return self