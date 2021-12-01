#!/usr/bin/env python3
import sys
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path

def dfDiff(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    merge = df1.merge(df2, how='outer', indicator=True)
    return merge[merge['_merge'] == 'left_only'].drop(columns="_merge")

def dw_diff(d1: Path, d2: Path) -> bool:
    errors = False
    for f_left in d1.rglob('*.arr'):
        f_right = (d2 / f_left.relative_to(d1)).with_suffix('.arr')
        print(f"Checking {f_left} vs. {f_right}.", end='', flush=True)

        if not f_right.exists():
            errors = True
            print(f"Error with {f_right}:")
            print("> File doesn't exist yet")
            continue

        print(".", end='', flush=True)
        
        df_left = pd.read_feather(f_left).sort_index(axis=1).set_index(['id', 'network'])
        df_right = pd.read_feather(f_right).sort_index(axis=1).set_index(['id', 'network'])
        
        c_left = df_left.columns
        c_right = df_right.columns
        
        if not c_right.symmetric_difference(c_left).empty:
            errors = True
            print(f" Error with {f_right}:")
            print("> NEW has " + ", ".join(c_right.difference(c_left)))
            print("> OLD has " + ", ".join(c_left.difference(c_right)))
            print("> Common  " + "," .join(c_right.intersection(c_left)))
            
            continue

        print(".", end='', flush=True)

        merge = df_left.merge(df_right, how='outer', indicator=True)
        left_merge = merge[merge['_merge'] == 'left_only']
        if not left_merge.empty:
            errors = True
            print(f" Errors with {f_left}:")
            print("LEFT ONLY (missing on right)")
            print(left_merge)

        right_merge = merge[merge['_merge'] == 'right_only']
        if not right_merge.empty:
            print(f" Warning with {f_right}:")
            print("RIGHT ONLY (missing on left)")
            print(right_merge)
        
        if not left_merge.empty or not right_merge.empty:
            continue
        
        print(".", end='', flush=True)

        try:
            assert_frame_equal(df_left, df_right, check_like=True)
        except AssertionError as e:
            errors = True
            print(f" Error with {f_right}:")
            print(e)
            continue
    
        print(" OK")

    return errors

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} datawarehouse1 datawarehouse2", file=sys.stderr)
        exit(2)

    d1 = Path(sys.argv[1])
    d2 = Path(sys.argv[2])
    if dw_diff(d1, d2):
        exit(1)
            
    print("All OK!")
    exit(0)