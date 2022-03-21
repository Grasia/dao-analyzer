#!/bin/env python
import sys
import pandas as pd

df = pd.read_feather(sys.argv[1])
print(df)
print(df.dtypes)
