from typing import Any

import pandas as pd
from millify import millify

from .....business.transfers import HierarchicalData
from . import IMetricStrategy
from .... import pandas_utils as pd_utl

class StAssetsValues(IMetricStrategy):
    DEFAULT_TOP_PCT = 0.5

    DEFAULT_VALUES_COLS = ['usdValue', 'eurValue', 'ethValue', 'balanceFloat']

    def __init__(self, idx_col: str, cmp_col: str='usdValue', values_cols: str = DEFAULT_VALUES_COLS, top_pct: float = DEFAULT_TOP_PCT):
        self._idx_col = idx_col
        self._cmp_col = cmp_col
        self._values_cols = values_cols
        self._top_pct = top_pct
    
    @property
    def _group_path(self):
        return [['network'], [self._idx_col, 'name'], ['symbol']]

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[df[self._cmp_col] > 0].copy()

        df['name'] = df['name'].fillna(df[self._idx_col].str.slice(0,8) + '...')
        df['name'] = df['name'].astype(str)

        return df

    def _build_id(self, dfg, i):
        if i > 0:
            index = [x[0] for x in self._group_path[:i]]
            # numpy.core._exceptions._UFuncNoLoopError: ufunc 'add' did not contain a loop with signature matching types (dtype('<U6'), dtype('float64')) -> None
            return 'total/' + dfg[index].astype(str).agg('/'.join, axis=1)
        else:
            return 'total'

    def _customData(self, dfg):
        if isinstance(dfg, pd.Series):
            return dfg[self._values_cols].apply(millify, precision=2).tolist()
        return pd.Series(dfg[self._values_cols].applymap(millify, precision=2).values.tolist())

    def _flatten(self, lists):
        ret = []

        for i in lists:
            if isinstance(i, list):
                ret.extend(i)
            else:
                ret.append(i)

        return ret

    def _valueBy(self, df, k=1):
        aux = df.groupby(self._flatten(self._group_path[:k]))[self._values_cols].sum()
        return aux

    def _value(self, dfg, i):
        if i < len(self._group_path):
            return 0
        else:
            return dfg[self._cmp_col]

    def process_data(self, df: pd.DataFrame) -> Any:
        df = self.clean_df(df)
        df = df.set_index([self._idx_col, 'network'])

        top, rest = pd_utl.top_rest_daos(df, idx=self._idx_col, value_col=self._cmp_col, top_pct=self._top_pct)

        df_trees = []
        if not top.empty:
            for i, level in enumerate(self._group_path):
                df_tree = pd.DataFrame(columns=['id', 'label', 'parent', 'value', 'customData'])
                dfg = self._valueBy(top, i+1).reset_index()
                
                _id = level[0]
                _label = level[-1]

                df_tree['label'] = dfg[_label].copy().fillna(dfg[_id])
                df_tree['parent'] = self._build_id(dfg, i)
                df_tree['id'] = self._build_id(dfg, i+1)
                df_tree['customData'] = self._customData(dfg)
                df_tree['value'] = self._value(dfg, i+1)

                df_trees.append(df_tree)

        # Now to append the 'Rest' value (symbols parents)
        if not rest.empty:
            df_tree = pd.DataFrame(columns=['id', 'label', 'parent', 'value', 'color', 'customData'])
            dfg = rest.groupby(['network'])[self._values_cols].sum().reset_index()
            df_tree['parent'] = self._build_id(dfg, 1)
            df_tree['id'] = df_tree['parent'] + '/other'
            df_tree['label'] = '<i>Rest of DAOs</i>'
            df_tree['value'] = 0
            df_tree['customData'] = self._customData(dfg)
            df_trees.append(df_tree)

            # Now to append the SYMBOLS into the 'Rest'
            df_tree = pd.DataFrame(columns=['id', 'label', 'parent', 'value', 'color', 'customData'])
            dfg = rest.groupby(['network', 'symbol'])[self._values_cols].sum().reset_index()
            df_tree['parent'] = self._build_id(dfg, 1) + '/other'
            df_tree['id'] = df_tree['parent'] + '/' + dfg['symbol']
            df_tree['label'] = dfg['symbol']
            df_tree['value'] = self._value(dfg, i+1)
            df_tree['customData'] = self._customData(dfg)
            df_trees.append(df_tree)

        df_trees.append(pd.DataFrame({
            'id': ['total'],
            'label': ['All Networks'],
            'parent': [''],
            'value': [0],
            'customData': [self._customData(df[self._values_cols].sum())],
        }))

        df_ret = pd.concat(df_trees, ignore_index=True, axis=0)
        return HierarchicalData.from_df(df_ret)