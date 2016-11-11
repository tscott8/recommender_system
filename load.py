import numpy as np
import pandas as pd
from sklearn.datasets.base import Bunch


def get_column(df, col):
    index = 0
    if col in df.columns.values:
        index = df.columns.values.tolist().index(col)
    return df.values[:,index]

df = pd.read_csv('datasets/SongCSV3.csv')
#columns = df.columns.values
print(df.columns.values)
#data = df.values
np.set_printoptions(threshold=np.inf)
column = get_column(df, 'ArtistName')
for i in column:
    print(i)
    