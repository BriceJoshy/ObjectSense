import csv

import pandas as pd


df = pd.read_csv("file.csv", delim_whitespace=True)
print(df)
