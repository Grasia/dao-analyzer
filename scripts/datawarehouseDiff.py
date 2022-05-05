#!/usr/bin/env python3
import json
import sys
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path

SKIP_COLUMNS = ['usdValue', 'eurValue', 'ethValue', 'balanceFloat']

def dfDiff(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    merge = df1.merge(df2, how='outer', indicator=True)
    return merge[merge['_merge'] == 'left_only'].drop(columns="_merge")

def dfRead(f):
    df = pd.read_feather(f).set_index(['network', 'id'])
    df = df.sort_index().sort_index(axis=1) # Sorting columns and index
    df = df.drop(columns=SKIP_COLUMNS, errors='ignore')
    return df

def md_diff(d1: Path, d2: Path) -> bool:
    errors = False
    for f_left in d1.rglob('metadata.json'):
        f_right = d2 / f_left.relative_to(d1)

        with open(f_left, 'r') as f:
            j_left = json.load(f)
        with open(f_right, 'r') as f:
            j_right = json.load(f)

        if j_left['errors']:
            print(f'Error found in {f_left}: {j_left["errors"]}')
            errors = True
        if j_right['errors']:
            print(f'Error found in {f_right}: {j_right["errors"]}')
            errors = True
        
        for cid, cdata in j_left['metadata'].items():
            lb = cdata['block']
            rb = j_right['metadata'][cid]['block']
            if lb['id'] != rb['id']:
                errors = True
                print("> Metadata block mismatch")
                print(f"LEFT:  {lb}")
                print(f"RIGHT: {rb}, number: ")

    return errors

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
        
        df_left = dfRead(f_left)
        df_right = dfRead(f_right)
        
        c_left = df_left.columns
        c_right = df_right.columns
        
        if not c_right.symmetric_difference(c_left).empty:
            errors = True
            print(f"\nError with {f_right}:")
            print("> NEW has " + ", ".join(c_right.difference(c_left)))
            print("> OLD has " + ", ".join(c_left.difference(c_right)))
            print("> Common  " + "," .join(c_right.intersection(c_left)))
            
            continue

        print(".", end='', flush=True)

        if (df_left.shape != df_right.shape):
            errors = True
            print(f'\nDifferent shape with {f_right}:')
            print("> LEFT  has", df_left.shape)
            print("> RIGHT has", df_right.shape)

        print(".", end='', flush=True)

        # dfc = df_left.compare(df_right)
        # if not dfc.empty:
        #     errors = True
        #     print(dfc)
        #     continue

        print(".", end='', flush=True)

        merge = df_left.merge(df_right, how='outer', indicator=True)
        left_merge = merge[merge['_merge'] == 'left_only']
        if not left_merge.empty:
            errors = True
            print(f"\nErrors with {f_left}:")
            print("LEFT ONLY (missing on right)")
            print(left_merge)

        right_merge = merge[merge['_merge'] == 'right_only']
        if not right_merge.empty:
            print(f"\nWarning with {f_right}:")
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
    if md_diff(d1, d2):
        exit(1)
    else:
        print("Metadata OK...")
    
    if dw_diff(d1, d2):
        exit(1)
            
    print("All OK!")
    exit(0)