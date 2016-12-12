# # -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:38:13 2016

@author: Tyler
"""

import numpy as np
import spotipy
import spotipy.util as util
from file_handler import FileHandler
from sklearn import datasets
from sklearn.datasets.base import Bunch
from sklearn.preprocessing import normalize
import webbrowser


class Retriever:

    def __init__(self):
        # SPOTIFY
        self.API_KEY = "39af097001da491989713c62c34bc5f5"
        self.API_SECRET = "a57a6d0188ba402f867ad71107735cd0"
        self.username = str(12145477386)
        self.scope = 'user-library-read'
        self.token = spotipy.util.prompt_for_user_token(username=self.username,
                                                        scope=self.scope,
                                                        client_id=self.API_KEY,
                                                        client_secret=self.API_SECRET,
                                                        redirect_uri=None)
        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
        else:
            print ("Can't get token for", self.username)
        self.fh = FileHandler()

    def find_track(self, title):
        result = self.sp.search(q=title, limit=1)['tracks']['items'][0]
        print(result['name'], '-',result['artists'][0]['name'])
        webbrowser.open_new_tab(result['preview_url'])
        return result['uri'], result['artists'][0]['uri'], title, result['artists'][0]['name']

    def get_similar_artists(self, artist_uri, sample_size=10):
        # artist = self.sp.artist(artist_uri)
        similar_artists = self.sp.artist_related_artists(artist_uri)
        sa = []
        for artist in similar_artists['artists']:
            sa += [[artist['name'], artist['uri']]]
        return sa[:sample_size]

    def get_artist_all_tracks(self, artist_uri, sample_size=5):
        artist_albums = self.sp.artist_albums(artist_uri)
        all_tracks = []
        for album in artist_albums['items'][:sample_size]:
            album_uri = album['uri']
            tracks = self.sp.album_tracks(album_uri)
            for track in tracks['items']:
                all_tracks += [[track['name'], track['uri']]]
        return all_tracks

    def get_audio_features(self, tracks):
        features = []
        for i, track in enumerate(tracks):
            features += [self.sp.audio_features(track[1])]
        return features

    def build_dataset(self, data, labels):
        headers = np.array(['loudness', 'tempo', 'speechiness', 'key',
                   'valence', 'acousticness', 'liveness', 'instrumentalness',
                   'energy','danceability', 'time_signature', 'duration_ms'])
        headers.sort()
        dataset = Bunch()
        dataset['headers'] = headers
        dataset['labels'] = labels
        dataset['data'] = []
        for track_list in data:
            for feature_list in track_list:
                row = []
                for i, feature in enumerate(headers):
                    row += [feature_list[headers[i]]]
                dataset['data'] += [row]
        dataset['data'] = np.array(dataset['data'])
        dataset['labels'] = np.array(dataset['labels'])
        np.set_printoptions( suppress=True, threshold=20, linewidth=140, formatter = dict( float = lambda x: "%.3f" % x ))
        return dataset

    def check_db(self, track):
        return self.fh.check_for_file(song_title=track)

    def batch_audio_features(self,track_lists):
        all_ids = []
        all_labels = []
        all_features = []
        feature_sets = []
        for track_list in track_lists:
            for track in track_list:
               all_labels += [track]
               all_ids += [track[1]]
#        all_tracks_set = set(all_tracks)
 #       print(all_tracks_set)
        feature_sets = []
        while len(all_ids) > 50 :
            feature_sets += [all_ids[:50]]
            print(len(all_ids))
            del all_ids[:50]
        feature_sets += [all_ids[:]]
        
        for feature_set in feature_sets:
            all_features += [self.sp.audio_features(feature_set)]
        return all_features, all_labels
        
    def spotify_retrieve(self, track):
        track_uri, artist_uri, track_name, artist_name = self.find_track(track)
        similar_artists = self.get_similar_artists(artist_uri)
        tracks_for_clustering = []
        for similar_artist in similar_artists:
            sa_all_tracks = self.get_artist_all_tracks(similar_artist[1])
            tracks_for_clustering += [np.array(sa_all_tracks)]
        tracks_for_clustering += [np.array([[track_name, track_uri]])]
#        print(len(tracks_for_clustering))
        all_features, all_labels = self.batch_audio_features(tracks_for_clustering)
        #print(np.array(all_features))
#        all_features = []
#        all_labels = []
#        for track_list in tracks_for_clustering:
#            print(set(track_list))
#            features = []
#            for track in track_list:
#                features += [track[1]]
#                all_labels += [track]
##            for sample in range(len(features)):
##                if sample % 50 is 0:
##                    features = self.sp.audio_features([features[:sample-50], features[sample+50:]])
##                    all_features += [features]
#            print(len(features))
#            features = self.sp.audio_features(features)
#            all_features += [features]
        # print(all_labels)
        dataset = self.build_dataset(all_features, all_labels)
        np.set_printoptions(threshold=np.nan)
        return dataset

    def db_retrieve(self, track):
        track_uri, artist_uri, track_name, artist_name = self.find_track(track)
        return self.fh.retrieve_file(track_name, artist_name)

    def retrieve(self, track):
        dataset = []
        if self.check_db(track) is True:
            dataset = self.db_retrieve(track)
        else:
            dataset = self.spotify_retrieve(track)
        # self.fh.write_file()
        return dataset
#
#ret = Retriever()
#dataset = ret.retrieve('Radioactive')
#print(len(dataset.labels), dataset.labels)
#print(len(dataset.data), dataset.data)
