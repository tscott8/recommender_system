from clusterer import Clusterer
import webbrowser


track_name = input("Enter the name (artist optional) of a song: ") or 'White Spirit Feed Me'
c = Clusterer(track_name=track_name)
results = c.get_target_cluster()

#ids = []
tracks = []
for i, item in enumerate(results):
    tracks += [c.ret.sp.track(item[1])]
#for j,t in enumerate(ids):
#    tracks += [c.ret.sp.track(t)]
for track in tracks:
    print ('track:', track['name'], '-', track['album']['artists'][0]['name'])
    print ('preview:', track['preview_url'])
    webbrowser.open_new_tab(track['preview_url'])
    print ('full:', 'https://play.spotify.com/track/'+ track['id'])
    print ('cover art:', track['album']['images'][0]['url'],track['preview_url'])
    
c.plot_clusters()
