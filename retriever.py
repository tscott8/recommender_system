# # -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:38:13 2016

@author: Tyler
"""

import numpy as np
import spotipy
import spotipy.util as util
from file_handler import FileHandler
from sklearn.datasets.base import Bunch
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
        # Search for the track and return the first result
        result = self.sp.search(q=title, limit=1)['tracks']['items'][0]
        return title, result['uri'], result['artists'][0]['name'], result['artists'][0]['uri'], result['preview_url']

    def get_similar_artists(self, artist_uri, sample_size=10):
        # artist = self.sp.artist(artist_uri)
        # get all related artists to the one in question
        similar_artists = self.sp.artist_related_artists(artist_uri)
        sa = []
        for artist in similar_artists['artists']:
            sa += [[artist['name'], artist['uri']]]
        return sa[:sample_size]

    def get_artist_all_tracks(self, artist_uri, sample_size=10):
        # get all of the albums of each artist
        artist_albums = self.sp.artist_albums(artist_uri)
        # then get all the tracks in each of those albums
        all_tracks = []
        for album in artist_albums['items'][:sample_size]:
            album_uri = album['uri']
            tracks = self.sp.album_tracks(album_uri)
            for track in tracks['items']:
                all_tracks += [[track['name'], track['uri']]]
        return all_tracks

    def get_audio_features(self, tracks):
        # get the audio_features that define each track numerically
        features = []
        for i, track in enumerate(tracks):
            features += [self.sp.audio_features(track[1])]
        return features

    def build_dataset(self, data, labels):
        # build an array of the features we want to use for clustering
        headers = np.array(['loudness', 'tempo', 'speechiness', 'key',
                   'valence', 'acousticness', 'liveness', 'instrumentalness',
                   'energy','danceability', 'time_signature', 'duration_ms'])
        headers.sort()
        # initialize the dataset modelled after sklearns
        dataset = Bunch()
        dataset['headers'] = headers
        dataset['labels'] = labels
        dataset['data'] = []
        # loop through the track_list of features, building the array, trimming
        # unwanted features and associating the proper index for each set of features
        for track_list in data:
            for feature_list in track_list:
                row = []
                for i, feature in enumerate(headers):
                    row += [feature_list[headers[i]]]
                dataset['data'] += [row]
        # make them nice np.arrays for printing
        dataset['data'] = np.array(dataset['data'])
        dataset['labels'] = np.array(dataset['labels'])
        # pretty printing
        np.set_printoptions( suppress=True, threshold=20, linewidth=140,
                            formatter = dict( float = lambda x: "%.3f" % x ))
        return dataset

    def check_db(self, track):
        # inquire if the data has been used/saved before
        return self.fh.check_for_file(song_title=track)

    def batch_audio_features(self,track_lists):
        # since spotipy only allows for features requests of
        # 50 tracks at a time, we needed to develop a way to
        # collect features for track lists larger than that.
        all_ids = []
        all_labels = []
        all_features = []
        feature_sets = []
        # split the tracks from their ids
        for track_list in track_lists:
            for track in track_list:
               all_labels += [track]
               all_ids += [track[1]]

        # all_tracks_set = set(all_tracks)
        # print(all_tracks_set)
        # split the ids into subsets of 50
        while len(all_ids) > 50 :
            feature_sets += [all_ids[:50]]
            del all_ids[:50]
        # add whatever ids still remain
        feature_sets += [all_ids[:]]
        # run the request to get the audio_features data
        for feature_set in feature_sets:
            all_features += [self.sp.audio_features(feature_set)]
        return all_features, all_labels

    def spotify_retrieve(self, track):
        # get the track data
        track_name, track_uri, artist_name, artist_uri, preview_url = self.find_track(track)
        # output the track and artist name that was found
        print(track_name, '-', artist_name)
        # play 30 second sample of the song in the browser
        webbrowser.open_new_tab(preview_url)
        # get the similar_artists
        similar_artists = self.get_similar_artists(artist_uri)
        print('Gathering songs from', len(similar_artists), 'artists please wait...')
        # get all the tracks for all the artists to do all the things!
        tracks_for_clustering = []
        for i,similar_artist in enumerate(similar_artists):
            print(str(i+1)+'. '+similar_artist[0])
            sa_all_tracks = self.get_artist_all_tracks(similar_artist[1])
            tracks_for_clustering += [np.array(sa_all_tracks)]

        # add the original track searched for into the set
        tracks_for_clustering += [np.array([[track_name, track_uri]])]
        # get the audio_features for each track
        all_features, all_labels = self.batch_audio_features(tracks_for_clustering)
        # build the dataset for Clustering
        dataset = self.build_dataset(all_features, all_labels)
        print('Clustering', len(dataset.data), 'songs, please wait...')
        # pretty print!
        np.set_printoptions(threshold=np.nan)
        return dataset

    def db_retrieve(self, track):
        # get the track info and dataset
        track_name, track_uri, artist_name, artist_uri, preview_url = self.find_track(track)
        return self.fh.retrieve_file(track_name, artist_name)

    def retrieve(self, track):
        # retrieve dataset from spotify or database
        dataset = []
        if self.check_db(track) is True:
            dataset = self.db_retrieve(track)
        else:
            dataset = self.spotify_retrieve(track)
        # self.fh.write_file()
        return dataset

    def spot_reccomendations(self, track):
        # get recommendations to compare against ours
        track_name, track_uri, artist_name, artist_uri, preview_url = self.find_track(track)
        results = self.sp.recommendations(seed_artists=[artist_uri],
                                          seed_tracks=[track_uri], limit=20)
        tracks = []
        for item in results['tracks']:
            tracks += [self.sp.track(item['uri'])]
        return tracks

# testing stuff...
# ret = Retriever()
# dataset = ret.retrieve('Radioactive')
# print(len(dataset.labels), dataset.labels)
# print(len(dataset.data), dataset.data)
