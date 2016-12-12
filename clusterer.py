import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from retriever import Retriever
from sklearn import metrics
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.datasets.base import Bunch
from sklearn.preprocessing import normalize

class Clusterer:
    def __init__(self, ret=Retriever(), track_name='Radioactive'):
        self.ret = ret
        self.dataset = self.ret.retrieve(track_name)
        # get the data set
        self.data = self.dataset.data.tolist()
        # get the track ids
        self.track_ids = self.dataset.labels.tolist()
        self.k =  KMeans(init='k-means++', n_clusters=10, algorithm='auto').fit(self.data)
        np.set_printoptions(threshold=np.nan)

    def get_target_cluster(self):
        # the index into data for the song we are looking for
        index = len(self.data) - 1
        cluster_number = self.k.labels_[index]
        # get the index of each item in the cluster
        similar_songs_index = [i for i, item in enumerate(self.k.labels_) if item == cluster_number]
        #print(similar_songs_index)
        # loop through similar_songs and print out the song
        #   that is associated with that index
        similar_songs = [self.track_ids[i] for i in similar_songs_index]
        del similar_songs[-1]
        # print("Similar Songs")
        # for x in similar_songs:
        # 	print(x)
        # np.set_printoptions(threshold=np.nan)
        return np.array(similar_songs)

    def gather_clusters(self):
        cluster_nums = np.unique(self.k.labels_)
        clusters = []
        for i, cluster_number in enumerate(cluster_nums):
            songs_index = [i for i, item in enumerate(self.k.labels_) if item == cluster_number]
            songs = [self.track_ids[i] for i in songs_index]
            clusters[i] = [songs]
        return clusters

    def plot_clusters(self):
        data = scale(self.dataset.data)
        n_samples, n_features = data.shape
        n_digits = len(np.unique(self.track_ids))
        labels = self.track_ids
        reduced_data = PCA(n_components=2).fit_transform(data)
        kmeans = KMeans(init='k-means++', n_clusters=20, algorithm='auto')
        kmeans.fit(reduced_data)
        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].
        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
        y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Obtain labels for each point in mesh. Use last trained model.
        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.figure(1)
        plt.clf()
        plt.imshow(Z, interpolation='nearest',
                   extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                   cmap=plt.cm.Paired,
                   aspect='auto', origin='lower')
        plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
        # Plot the centroids as a white X
        centroids = kmeans.cluster_centers_
#        plt.scatter(centroids[:, 0], centroids[:, 1],
#                    marker='x', s=85, linewidths=3,
#                    color='w', zorder=10)
        plt.title('K-means clustering on songs (PCA-reduced data)')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())
        plt.show()


# c = Clusterer()
# print(c.get_target_cluster())
# c.plot_clusters()
