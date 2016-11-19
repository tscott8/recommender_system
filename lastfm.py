import pylast as last
import numpy as np

API_KEY = "63a291a5de6b3a0313b795520d85e4d6"
API_SECRET = "02f60c5dacb55716b29b2e58e09fc3aa"

network = last.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

track = network.get_track(artist="Imagine Dragons", title="Radioactive")
print('Song: ', track.title)
artist = network.get_artist(track.artist)
print('Artist: ',artist)
# print('Top Tracks: ', artist.get_top_tracks(limit=10))

similar_artists = artist.get_similar(limit=10)
similar_artists_names = []
for artist in similar_artists:
    similar_artists_names += [artist.item.name]
# similar_artists = temp[:]
similar_artists_names = np.array(similar_artists_names)
print('Similar Artists: ', similar_artists_names)

sim_artist_top_tracks = []
for i, sim_artist in enumerate(similar_artists):
    artist_top_tracks = sim_artist.item.get_top_tracks(limit=10)
    temp = []
    for j, top_track in enumerate(artist_top_tracks):
        temp += [top_track.item.title]
    sim_artist_top_tracks += [temp]
sim_artist_top_tracks = np.array(sim_artist_top_tracks)
print('Similar Artists Top Tracks: ', sim_artist_top_tracks)
