# # -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:38:13 2016

@author: Tyler
"""

import spotipy
import spotipy.util as util
import numpy as np
# # SPOTIFY
API_KEY = "39af097001da491989713c62c34bc5f5"
API_SECRET = "a57a6d0188ba402f867ad71107735cd0"
# API_REDIRECT_URI = "http://localhost:8080"
# REDIRECT_URL = "http://localhost:8080/?code=AQBnhaoBNyyqcZTt2M-24eTW1wGUgt93fzKaFVB09Iyp77tKGvaUbbG3mKphbSehc7Mn4is1biN29xmg3DKH4l3fbsQi_TWzbGnC6BDuPQpVRbKTZeGJ58joonOEqhf0DRo15WRfRP6kX3cLmyOShgeXWXUGerimbSirRNFVJz7_lhG3hDRS_z5TqXMuszpN6SMlPpjZ3d0Sj-spfrE"
# #TOKEN = "AQBnhaoBNyyqcZTt2M-24eTW1wGUgt93fzKaFVB09Iyp77tKGvaUbbG3mKphbSehc7Mn4is1biN29xmg3DKH4l3fbsQi_TWzbGnC6BDuPQpVRbKTZeGJ58joonOEqhf0DRo15WRfRP6kX3cLmyOShgeXWXUGerimbSirRNFVJz7_lhG3hDRS_z5TqXMuszpN6SMlPpjZ3d0Sj-spfrE"
username = str(12145477386)
#
scope = 'user-library-read'
token = spotipy.util.prompt_for_user_token(username=username,
                                           scope=scope,
                                           client_id=API_KEY,
                                           client_secret=API_SECRET,
                                           redirect_uri=None)

#sp = spotipy.Spotify(auth = token)
# #user = sp.user(USERNAME)
# #print(user)
# # results = sp.search(q='weezer', limit=20)
# # for i, t in enumerate(results['tracks']['items']):
# #     print (' ', i, t['name'])
# track_id = ''
# results = sp.search(q='Imagine Dragons', limit=20)
# for i, t in enumerate(results['tracks']['items']):
#     print (' ', i, t['name'])
#     if t['name'] == 'Radioactive':
#         track = t['id']
#         break
# features = sp.audio_features([track(track_id)]
# print(sp.me())
# print(features)
# shows a user's playlists (need to be authenticated via oauth)

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print ("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

def find_track(input):
    result = sp.search(q=input, limit=1)['tracks']['items'][0]
    return result['uri'], result['artists'][0]['uri']

def get_similar_artists(artist_uri):
    # artist = sp.artist(artist_uri)
    similar_artists = sp.artist_related_artists(artist_uri)
    sa = []
    for artist in similar_artists['artists']:
        sa += [[artist['name'], artist['uri']]]
    return sa[:5]

def get_artist_all_tracks(artist_uri):
    artist_albums = sp.artist_albums(artist_uri)
    all_tracks = []
    for album in artist_albums['items'][:5]:
        album_uri = album['uri']
        tracks = sp.album_tracks(album_uri)
        for track in tracks['items']:
            all_tracks += [[track['name'], track['uri']]]
    return all_tracks

def get_audio_features(tracks):
    features = []
    for i, track in enumerate(tracks):
        features += [sp.audio_features(track[1])]
    return features
    
if token:
    sp = spotipy.Spotify(auth=token)
    track_uri, artist_uri = find_track('Radioactive')
    print(sp.audio_features([track_uri]))
    # print(track_uri, artist_uri)
    similar_artists = get_similar_artists(artist_uri)
    # print(np.array(similar_artists))
    tracks_for_clustering = []
    for similar_artist in similar_artists:
        sa_all_tracks = get_artist_all_tracks(similar_artist[1])
        tracks_for_clustering += [sa_all_tracks]
    # print(np.array(tracks_for_clustering))
    #features_for_clustering = get_audio_features(tracks_for_clustering)
    all_features = []
    for track_list in tracks_for_clustering:
        features = []
        for track in track_list:
            features += [track[1]]
        features = sp.audio_features(features)
        all_features += [features]
    print(np.array(all_features))
    #print(tracks_for_clustering)
#   artist = sp.artist(da_track['artists'][0]['name'])
#   print(artist)
    #tracks = sp.current_user_saved_tracks(limit=50)
    #show_tracks(tracks)
    #features = []
#    for i, item in enumerate(tracks['items']):
#        track = item['track']['id']
#        features += [track]
#    features = sp.audio_features(features)
 #  print(np.array(features))
    #for playlist in playlists['items']:
#        if playlist['owner']['id'] == username:
#            print()
#            print (playlist['name'])
#            print ('  total tracks', playlist['tracks']['total'])
#            results = sp.user_playlist(username, playlist['id'],
#                fields="tracks,next")
#            tracks = results['tracks']
#            show_tracks(tracks)
#            while tracks['next']:
#                tracks = sp.next(tracks)
#                show_tracks(tracks)
else:
    print ("Can't get token for", username)
