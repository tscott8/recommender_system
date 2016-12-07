from sklearn.cluster import KMeans
from sklearn.datasets.base import Bunch
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
from retriever import Retriever

from sklearn import datasets

ret = Retriever()
dataset = ret.retrieve('Radioactive')

# get the data set
data = dataset.data.tolist()

# get the track ids
track_ids = dataset.labels.tolist()

k = KMeans(n_clusters=20).fit(data)

# the index into data fo the song we are looking for
index = len(data) - 1

cluster_number = k.labels_[index]

# get the index of each item in the cluster
similar_songs_index = [i for i, item in enumerate(k.labels_) if item == cluster_number]

#print(similar_songs_index)

# loop through similar_songs and print out the song
#   that is associated with that index
similar_songs = [track_ids[i] for i in similar_songs_index]
del similar_songs[-1]

print("Similar Songs")
for x in similar_songs:
	print(x)