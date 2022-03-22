"""
   Descp: Tabular data transfer for use in datatables

   Created on: 16-mar-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
from __future__ import annotations
from typing import Dict, List, Any

from dash.dash_table.Format import Format
import pandas as pd

class TabularData():
    def __init__(self):
        self._columns = {}
        self.data = []

    @property
    def columns(self) -> List[Dict[str,str]]:
        return [{'id': id, **rest} for id,rest in self._columns.items()]

    @staticmethod
    def from_df(df: pd.DataFrame) -> TabularData:
        def _t(dtype) -> str:
            if pd.api.types.is_numeric_dtype(dtype):
                return 'numeric'
            return None
        
        df = df.reset_index()
        self = TabularData()
        for id,dtype in df.dtypes.iteritems():
            self._columns[id] = {'name': id}
            if _t(dtype):
                self._columns[id]['type'] = _t(dtype)

        self.data = df.to_dict('records')
        return self

    def _set_column_thing(self, thing, newc: Dict[str, Any]) -> TabularData:
        for id,t in newc.items():
            if id in self._columns:
                self._columns[id][thing] = t
        
        return self
    
    def set_column_names(self, newc: Dict[str, str]) -> TabularData:
        """Sets the column names given the id

        Args:
            newc (Dict[str, str]): A dict of id:'Column Name'
        """
        return self._set_column_thing('name', newc)
    
    def set_column_formats(self, newc: Dict[str, Format]) -> TabularData:
        return self._set_column_thing('format', newc)