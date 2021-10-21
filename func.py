from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
songs = pd.read_csv('songs.csv')


def find_song_database(name, artist, songs):
    result = songs[(songs.artist_name == str(artist))
                   & (songs.track_name == str(name))]
    if len(result) == 0:
        return None
    return result.drop(['track_name', 'artist_name', 'Cluster'], axis=1)


def find_similar(name, artist, songs):
    database = songs[songs.popularity > 0.5].reset_index(drop=True)
    indx_names = database[['track_name', 'artist_name', 'tempo', 'popularity',
                           'energy', 'danceability', 'valence', 'liveness',
                           'loudness', 'speechiness', 'Cluster']]
    songs_train = database.drop(['track_name', 'artist_name', 'tempo',
                                 'popularity', 'energy', 'danceability',
                                 'valence', 'liveness', 'loudness',
                                 'speechiness', 'Cluster'], axis=1)

    song = find_song_database(str(name), str(artist), database)

    if type(song) != type(None):

        indx_song = song.index

        cos_dists = cosine_similarity(songs_train, songs_train)
        indx_names.loc[:, ['result']] = cos_dists[indx_song[0]]

        indx_names = indx_names.sort_values(by=['result'], ascending=False)

        return indx_names[1:6].reset_index(drop=True)

    else:
        print("Song not found")
        return None


def playlist_song(name, artist, songs):
    list_songs = find_similar(str(name), str(artist), songs)

    if type(list_songs) != type(None):

        print('Playlist based on "' + str(name) + '" by ' + str(artist))
        recommended_music = []
        for i in np.arange(0, len(list_songs)):
            track_name = list_songs.track_name[i]
            artist_name = list_songs.artist_name[i]

            print(str(track_name) + ' - ' + str(artist_name))
            recommended_music.append(
                str(track_name) + ' - ' + str(artist_name) + '   ')
        return(str(recommended_music))

    return None
