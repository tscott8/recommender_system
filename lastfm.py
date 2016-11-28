import pylast as last
import numpy as np

#LASTFM
API_KEY = "63a291a5de6b3a0313b795520d85e4d6"
API_SECRET = "02f60c5dacb55716b29b2e58e09fc3aa"

network = last.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

track = network.get_track(artist="Imagine Dragons", title="Radioactive")
print('Song: ', track.title)
print(track.get_mbid)
artist = network.get_artist(track.artist)
print('Artist: ', artist)
#albums = artist.get_top_albums(limit=10)
#for m, album in enumerate(albums):
#    # album = network.get_album(album=album.ite)
#    tracks = album.item.get_tracks()
#    for track in tracks:
#        print (track.title)
# print('Top Tracks: ', artist.get_top_tracks(limit=10))

similar_artists = artist.get_similar(limit=10)
similar_artists_names = []
for artist in similar_artists:
    similar_artists_names += [artist.item.name]
# similar_artists = temp[:]
# similar_artists_names = np.array(similar_artists_names)
#print('Similar Artists: ', similar_artists_names)


#sim_artist_top_tracks = []
#for i, sim_artist in enumerate(similar_artists):
#    artist_top_tracks = sim_artist.item.get_top_tracks(limit=10)
#    temp = []
#    for j, top_track in enumerate(artist_top_tracks):
#        temp += [top_track.item.title]
#    sim_artist_top_tracks += [temp]
## sim_artist_top_tracks = np.array(sim_artist_top_tracks)
#print('Similar Artists Top Tracks: ', sim_artist_top_tracks)
sim_artist_top_albums_tracks = []
for sim_artist in similar_artists:
    artist_top_albums = sim_artist.item.get_top_albums(limit=10)
    temp1 = []
    for top_album in artist_top_albums:
        track_list = top_album.item.get_tracks()
        temp2 = []
        for track in track_list:
            temp2 += [track.title]
        temp1 += [top_album.item.title, temp2]
      #  temp1 += temp2
    sim_artist_top_albums_tracks += [sim_artist.item.name, temp1]
#sim_artist_top_albums_tracks = np.array(sim_artist_top_albums_tracks)
print('Similar Artists Top Albums ALL Tracks: ', sim_artist_top_albums_tracks)
