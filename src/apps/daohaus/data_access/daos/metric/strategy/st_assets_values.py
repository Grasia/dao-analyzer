from typing import Any

import pandas as pd
from millify import millify
from src.apps.common.business.transfers.hierarchical_data import HierarchicalData

from src.apps.common.data_access.daos.metric.imetric_strategy import IMetricStrategy
import src.apps.common.data_access.pandas_utils as pd_utl

class StAssetsValues(IMetricStrategy):
    DEFAULT_TOP_PCT = 0.5

    __values_cols = ['usdValue', 'eurValue', 'ethValue', 'balanceFloat']
    __idx_col = 'molochAddress'
    __group_path = [['network'], [__idx_col, 'name'], ['symbol']]
    __cmp_col = 'usdValue'

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df['name'] = df['name'].astype(str)
        df = df[df[self.__cmp_col] > 0]
        return df

    def _build_id(self, dfg, i):
        if i > 0:
            index = [x[0] for x in self.__group_path[:i]]
            # numpy.core._exceptions._UFuncNoLoopError: ufunc 'add' did not contain a loop with signature matching types (dtype('<U6'), dtype('float64')) -> None
            return 'total/' + dfg[index].astype(str).agg('/'.join, axis=1)
        else:
            return 'total'

    def _customData(self, dfg):
        if isinstance(dfg, pd.Series):
            return dfg[self.__values_cols].apply(millify, precision=2).tolist()
        return pd.Series(dfg[self.__values_cols].applymap(millify, precision=2).values.tolist())

    def _flatten(self, lists):
        ret = []

        for i in lists:
            if isinstance(i, list):
                ret.extend(i)
            else:
                ret.append(i)

        return ret

    def _valueBy(self, df, k=1):
        aux = df.groupby(self._flatten(self.__group_path[:k]))[self.__values_cols].sum()
        return aux

    def _value(self, dfg, i):
        if i < len(self.__group_path):
            return 0
        else:
            return dfg[self.__cmp_col]

    def process_data(self, df: pd.DataFrame) -> Any:
        print(df)
        df = self.clean_df(df)
        df = df.set_index([self.__idx_col, 'network'])
        
        print(df)
        print(df.describe())
        print("idx:", df.index)
        print("dtypes:", df.dtypes)


        top, rest = pd_utl.top_rest_daos(df, idx=self.__idx_col, value_col=self.__cmp_col, top_pct=self.DEFAULT_TOP_PCT)

        df_trees = []
        for i, level in enumerate(self.__group_path):
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
        df_tree = pd.DataFrame(columns=['id', 'label', 'parent', 'value', 'color', 'customData'])
        dfg = rest.groupby(['network'])[self.__values_cols].sum().reset_index()
        df_tree['parent'] = self._build_id(dfg, 1)
        df_tree['id'] = df_tree['parent'] + '/other'
        df_tree['label'] = '<i>Rest of DAOs</i>'
        df_tree['value'] = 0
        df_tree['customData'] = self._customData(dfg)
        df_trees.append(df_tree)

        # Now to append the SYMBOLS into the 'Rest'
        df_tree = pd.DataFrame(columns=['id', 'label', 'parent', 'value', 'color', 'customData'])
        dfg = rest.groupby(['network', 'symbol'])[self.__values_cols].sum().reset_index()
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
            'customData': [self._customData(df[self.__values_cols].sum())],
        }))

        df_ret = pd.concat(df_trees, ignore_index=True, axis=0)
        return HierarchicalData.from_df(df_ret)