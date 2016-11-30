# # -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:38:13 2016

@author: Tyler
"""

import spotipy
import spotipy.util as util
import numpy as np
from sklearn.datasets.base import Bunch


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


    def find_track(self, title):
        result = self.sp.search(q=title, limit=1)['tracks']['items'][0]
        print(result['name'], '-', result['artists'][0]['name'])
        return result['uri'], result['artists'][0]['uri']

    def get_similar_artists(self, artist_uri, sample_size=5):
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
    
    def build_dataset(self, data):
        headers = ['uri', 'loudness', 'mode', 'tempo', 'speechiness', 'key',
                   'valence', 'acousticness', 'liveness', 'instrumentalness', 'energy',
                   'danceability', 'time_signature', 'duration_ms']
 #       print('Headers:\n', np.array(headers))
        dataset = Bunch()
        dataset['headers'] = headers
        dataset['data'] = []
        for track_list in data:
            for feature_list in track_list:
                row = []
                for i, feature in enumerate(headers):
                    row += [feature_list[headers[i]]]
#                print(np.array(row))
                dataset['data'] += [row]
#               
        print(dataset)
        return dataset
        
    def check_db(self, track):
        print('Not yet implemented')
        return False

    def spotify_retrieve(self, track):
        track_uri, artist_uri = self.find_track(track)
        print(self.sp.audio_features([track_uri]))
        print(track_uri, artist_uri)
        similar_artists = self.get_similar_artists(artist_uri)
        print('SIMILAR ARTISTS:\n', np.array(similar_artists))
        tracks_for_clustering = []
        for similar_artist in similar_artists:
            sa_all_tracks = self.get_artist_all_tracks(similar_artist[1])
            tracks_for_clustering += [np.array(sa_all_tracks)]
        print('TRACKS FOR CLUSTERING:\n', np.array(tracks_for_clustering))
        #features_for_clustering = get_audio_features(tracks_for_clustering)
        all_features = []
        for track_list in tracks_for_clustering:
            features = []
            for track in track_list:
                features += [track[1]]
#            for sample in range(len(features)):
 #               if sample % 50 is 0:
  #                  features = self.sp.audio_features(features[sample-50:, :sample])
            features = self.sp.audio_features(features)
            all_features += [features]
        #print(np.array(all_features))
        dataset = self.build_dataset(all_features)
        return dataset

    def db_retrieve(self, track):
        print('Not yet implemented.')

    def retrieve(self, track):
        if self.check_db(track) is True:
            return self.db_retrieve(track)
        else:
            return self.spotify_retrieve(track)


ret = Retriever()
ret.retrieve('Radioactive')
