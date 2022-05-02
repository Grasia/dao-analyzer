"""
   Descp: Hierarchical data transfer for use in sunburst and treemaps

   Created on: 11-mar-2022

   Copyright 2022-2022 David Davó Laviña
        <ddavo@ucm.es>
"""
import pandas as pd
from millify import millify

class HierarchicalData():
    """
    * labels
    * parents
    * ids
    * values
    * customdata
    * total
    """

    def __init__(self):
        self.labels = []
        self.parents = []
        self.ids = []
        self.values = []
        self.customdata = []
        self.total = None
    
    @staticmethod
    def from_df(df: pd.DataFrame):
        self = HierarchicalData()
        self.labels = df['label'].to_list()
        self.parents = df['parent'].to_list()
        self.ids = df['id'].to_list()
        self.values = df['value'].to_list()
        if 'customData' in df.columns:
            self.customdata = df['customData'].to_list()
        self.total = df['value'].sum()
        self.total = millify(df['value'].sum(), precision=2) + '$'

        return self
    
    def to_dict(self):
        return {
            'ids': self.ids,
            'labels': self.labels,
            'parents': self.parents,
            'values': self.values,
            'customdata': self.customdata,
            'total': self.total,
        }
