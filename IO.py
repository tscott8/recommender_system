from clusterer import Clusterer
import webbrowser

# Get the user input track
track_name = input("Enter the name (artist optional) of a song: ") or 'Give it up Knife Party'

# Run the clustering on the track
c = Clusterer(track_name=track_name, alg_type='affprop')
results = c.get_target_cluster()
c.plot_clusters()
print('Graph saved to ./Database/clusters.png')

# convert the track ids returned from clustering back into track data
print('Loading 20 of', len(results), 'track recommendations, please wait...')
print()
shift_tracks = []
for i, item in enumerate(results):
    shift_tracks += [c.ret.sp.track(item[1])]

# output and save the recommended tracks to a file
def output_recommendations(source, filename, tracks):
    print(source+' Recommendations:')
    fout = open(filename, 'w')
    for track in tracks[:20]:
        print ('track:', track['name'], '-', track['album']['artists'][0]['name'])
        print ('track:', track['name'], '-', track['album']['artists'][0]['name'], file=fout)
        print ('preview:', track['preview_url'])
        print ('preview:', track['preview_url'], file=fout)
        preview_url = track['preview_url']
        if preview_url:
            webbrowser.open_new_tab(preview_url)
        print ('full:', 'https://play.spotify.com/track/'+ track['id'])
        print ('full:', 'https://play.spotify.com/track/'+ track['id'], file=fout)
        print ('cover art:', track['album']['images'][0]['url'])
        print ('cover art:', track['album']['images'][0]['url'], file=fout)
        print()
        print('', file=fout)
    fout.close()
    print('Track recommendations saved to ./Database/'+filename)
    print()

# compare to the recommended tracks given from spotify
spot_tracks = c.ret.spot_reccomendations(track_name)
output_recommendations(source='Shift',
                       filename='shift_recommendations_'+track_name+'.txt',
                       tracks=shift_tracks)
#output_recommendations(source='Spotify',
#                       filename='spotify_recommendations_'+track_name+'.txt',
 #                      tracks=spot_tracks)    
    
