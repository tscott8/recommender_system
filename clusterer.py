import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from retriever import Retriever
from sklearn import metrics
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize

class Clusterer:
    def __init__(self, ret=Retriever(), track_name='Radioactive', alg_type='affprop'):
        self.ret = ret                                    # initalize the Retriever class
        self.dataset = self.ret.retrieve(track_name)      # get the data set
        self.data = normalize(self.dataset.data.tolist()) # normalize the data
        self.track_ids = self.dataset.labels.tolist()     # get the track ids
        self.reduced_data = self.reduce_data()            # reduce the data
        self.alg_type = alg_type                          # get the algorithm type
        self.alg = self.run_clustering()                  # setup the clustering
        self.clusters = self.alg.fit(self.reduced_data)   # cluster the data

    def reduce_data(self):
        # not totally sure what this all does
        data = scale(self.dataset.data) # scale the data to more manageable size
        n_samples, n_features = data.shape
        n_digits = len(np.unique(self.track_ids))
        labels = self.track_ids
        reduced_data = PCA(n_components=2).fit_transform(data)
        return reduced_data

    def run_clustering(self):
        # determine what kind of clustering setup to run
        if self.alg_type is 'kmeans':
            kmeans = KMeans(init='k-means++', n_clusters=10, algorithm='auto')
            return kmeans
        if self.alg_type is 'affprop':
            affprop = AffinityPropagation()
            return affprop

    def get_target_cluster(self):
        index = len(self.data) - 1 # the index into data for the song we are looking for
        cluster_number = self.clusters.labels_[index] # the cluster we are looking in
        # get the index of each item in the cluster
        similar_songs_index = [i for i, item in enumerate(self.clusters.labels_) if item == cluster_number]
        # print(similar_songs_index)
        # loop through similar_songs and print out the song that is associated with that index
        similar_songs = [self.track_ids[i] for i in similar_songs_index]
        del similar_songs[-1]
        # print("Similar Songs")
        # for x in similar_songs:
        # 	print(x)
        return np.array(similar_songs)

    def plot_clusters(self):
        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = .02 # point in the mesh [x_min, x_max]x[y_min, y_max].
        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = self.reduced_data[:, 0].min() - 1, self.reduced_data[:, 0].max() + 1
        y_min, y_max = self.reduced_data[:, 1].min() - 1, self.reduced_data[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        # Obtain labels for each point in mesh. Use last trained model.
        Z = self.alg.predict(np.c_[xx.ravel(), yy.ravel()])
        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        fig = plt.figure(1)
        plt.clf()
        plt.imshow(Z, interpolation='nearest',
                   extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                   cmap=plt.cm.Paired,
                   aspect='auto', origin='lower')
        plt.plot(self.reduced_data[:, 0], self.reduced_data[:, 1], 'k.', markersize=2)
        # Plot the centroid of the target cluster as a white X
        cluster_number = self.clusters.labels_[len(self.data)-1]
        centroid_prime = self.alg.cluster_centers_[cluster_number]
        plt.scatter(centroid_prime[0], centroid_prime[1],
                 marker='x', s=84, linewidths=2, color='w', zorder=10)
        # centroids = self.alg.cluster_centers_
        # plt.scatter(centroids[:, 0], centroids[:, 1],
        #             marker='x', s=85, linewidths=2,
        #             color='w', zorder=10)
        plt.title(self.alg_type + ' clustering on songs (PCA-reduced data)')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())
        fig.savefig('clusters.png', dpi=400)
        plt.show()


# testing stuff...
# c = Clusterer()
# print(c.get_target_cluster())
# c.plot_clusters()
