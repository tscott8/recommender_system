from sklearn.cluster import KMeans
from sklearn.datasets.base import Bunch
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np

from sklearn import datasets


# get the data set
data = datasets.load_iris().data

k = KMeans(n_clusters=3).fit(data)

# the index into data fo the song we are looking for
index = len(data) - 1

cluster_number = k.labels_[index]

# get the index of each item in the cluster
similar_songs = [i for i, item in enumerate(k.labels_) if item == cluster_number]

print(similar_songs)

# loop through similar_songs and print out the song 
#   that is associated with that index