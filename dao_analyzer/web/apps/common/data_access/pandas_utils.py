"""
   Descp: Util for pandas interactions.

   Created on: 16-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from datetime import date
from typing import List, Any, Dict, Tuple
import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import DateOffset


EQ = 0
NEQ = 1
GT = 2
GTE = 3
LT = 4
LTE = 5


def filter_by_col_value(df: DataFrame, col: str, value: Any, 
filters: List[int]) -> DataFrame:
    """
    Filters rows by a column value with each filter on filters list.
    Arguments:
        * df = The data frame to filter.
        * col = column name which is selected to filter by.
        * value = The value which the column must ajust.
        * filters = A list of filter to apply on the data frame.
    Return:
        A filtered data frame copy.
    """
    dff: DataFrame = df
    for f in filters:
        if f == EQ:
            dff = dff.loc[dff[col] == value]
        elif f == NEQ:
            dff = dff.loc[dff[col] != value]
        elif f == GT:
            dff = dff.loc[dff[col] > value]
        elif f == GTE:
            dff = dff.loc[dff[col] >= value]
        elif f == LT:
            dff = dff.loc[dff[col] < value]
        elif f == LTE:
            dff = dff.loc[dff[col] <= value]
    
    return dff

# TODO: Delete this (stop using it)
def append_rows(df: DataFrame, row: List) -> DataFrame:
    dff = pd.DataFrame([pd.Series(row, index=df.columns)])
    return pd.concat([df, dff], join='outer', ignore_index=True)


def get_empty_data_frame(columns: List[str] = None) -> DataFrame:
    cols = columns if columns else list()
    return DataFrame(columns=cols)


def get_df_from_lists(rows: List[List], columns: List[str]) -> DataFrame:
    if not len(rows) == len(columns):
        raise Exception

    rows = rows if rows else list()
    columns = columns if columns else list()

    di_df: Dict = dict()
    for i, c in enumerate(columns):
        di_df[c] = rows[i]

    return DataFrame(di_df).infer_objects()


def is_an_empty_df(df: DataFrame) -> bool:
    return df.shape[0] == 0


def unix_to_date(df: DataFrame, col: str) -> DataFrame:
    dff: DataFrame = df.copy()
    dff.loc[:, col] = pd.to_datetime(dff.loc[:, col], unit='s').dt.date
    return dff


def transform_to_monthly_date(df: DataFrame, col: str) -> DataFrame:
    dff: DataFrame = df.copy()
    dff.loc[:, col] = dff[col].apply(lambda d: d.replace(day=1))
    return dff


def datetime_to_date(df: DataFrame, col: str) -> DataFrame:
    dff: DataFrame = df
    dff.loc[:, col] = dff[col].dt.date
    return dff


def count_cols_repetitions(df: DataFrame, cols: List[str], new_col: str)\
-> DataFrame:
    dff: DataFrame = df
    dff = dff.groupby(cols).size().reset_index(name=new_col)
    return dff


def sum_cols_repetitions(df: DataFrame, cols: List[str], new_col: str)\
-> DataFrame:
    dff: DataFrame = df
    dff = dff.groupby(cols).sum().reset_index()
    return dff


def get_monthly_serie_from_df(df: DataFrame, date_col: str, start: date = None) -> pd.DatetimeIndex:
    if df.empty and not start:
        raise ValueError("DataFrame can't be empty if no start provided")

    today = date.today().replace(day=1)
    start = start or df[date_col].min()

    return pd.date_range(start=start, end=today, freq=DateOffset(months=1))


def drop_duplicate_date_rows(df: DataFrame, dff: DataFrame, date_col: str) -> None:
    """
    Removes all duplicated date-rows from dff considering the df's ones.
    """
    mask = dff[date_col].isin(df[date_col])
    dff = dff.drop(dff[mask].index)

    return dff

def top_rest_daos(df: DataFrame, idx, value_col, top_pct: float=0.50) -> Tuple[DataFrame, DataFrame]:
    """
    Calculates the top DAOs of each network
    """
    dfsum = df.groupby([idx, 'network']).sum() # Calculating value of every DAO
    dfsum = dfsum.sort_values(['network', value_col]) # Sorting by network>value because group doesnt have sort_values
    gbsum = dfsum.groupby('network')
    cumval = gbsum[value_col].cumsum() / gbsum[value_col].sum() # Calculating the cummulative value

    topmask = cumval > top_pct

    # Getting the top/rest subsets
    top = dfsum[topmask]
    rest = dfsum[~topmask]

    # Applying them to the original dfs (keeping all data)
    top = df.loc[top.index]
    rest = df.loc[rest.index]

    return top, rest
