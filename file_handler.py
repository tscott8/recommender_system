import os
import pandas

class FileHandler:
    def __init__(self):
        self.url = './{}/{}.csv'

    
    def check_for_file(self, song_title, artist=''):
        if artist is not '':
            if os.path.isfile(self.url.format(artist, song_title)):
                return True
            else:
                return False
        else:
            rootDir = '.'
            possible_artists = []
            for dirName, subdirList, fileList in os.walk(rootDir):
                if song_title + '.csv' in fileList:
                    possible_artists.append(dirName.replace("./", ""))
            if len(possible_artists) > 1:
                return self.identify_artist(possible_artists)
            elif len(possible_artists) is 0:
                return False
            else:
                return True, possible_artists[0]


    def identify_artist(self, possible_artists):
        print("Mutliple files have been found for this song. ")
        for i, artist in enumerate(possible_artists):
            print("[{}] {}".format(i, artist))
        print("[{}] {}".format("X", "None"))

        got_good_answer = False
        while not got_good_answer:
            answer = input("Which artist is the one you want? ")
            if answer is "X":
                return False
            else:
                try:
                    print("Index: ", int(answer))
                    return True, possible_artists[int(answer)]
                except (ValueError, IndexError) as e:
                    print("Sorry, that value is not a recoginzed options. Please try a different number.")


    def retrieve_file(self, song_title, artist):
        if os.path.exists(self.url.format(artist, song_title)):
            df = pandas.DataFrame.from_csv(self.url.format(artist, song_title))
            data = df.values
            return data
        else:
            print("Sorry, that artist and/or song does not have a file.")
            return false


    def write_file(self, song_title, artist, cluster_data):
        df = pandas.DataFrame(cluster_data)
        if not os.path.exists(artist):
            os.makedirs(artist)
        df.to_csv(self.url.format(artist, song_title))

