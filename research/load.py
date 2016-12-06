import numpy as np
import pandas as pd
from sklearn.datasets.base import Bunch


def get_column(df, col):
    index = 0
    if col in df.columns.values:
        index = df.columns.values.tolist().index(col)
    return df.values[:,index]

df = pd.read_csv('datasets/EvolutionPopUSA.csv')
columns1 = df.columns.values[:10]
print(columns1)
columns2 = df.columns.values[-9:]
print(columns2)
columns = np.concatenate((columns1,columns2), axis=0)
# print(df.columns.values)
data1 = df.values[:,:9]
data2 = df.values[:,-9]
data = np.concatenate((data1,data2), axis=0)

print(data)
column = np.unique(get_column(df, 'artist_name_clean'))
print(column)
# for i in column:
#     print(i)
