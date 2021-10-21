import pickle
import streamlit as st
import pandas as pd
import func
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

df = pd.read_csv('songs.csv')
st.title('Music Recommend System')
musics_dict = pickle.load(open('music_dict.pkl', 'rb'))
musics = pd.DataFrame(musics_dict)
selected_music = st.selectbox(
    "Type or select a music from the dropdown",
    musics['track_name'].values
)
selected_artist = st.selectbox(
    "Type or select a music from the dropdown",
    musics['artist_name'].values
)

if st.button('Recommend'):
    df1 = func.find_similar(selected_music, selected_artist, df)
    print(df1)
    df1 = df1.drop(['result', 'track_name', 'artist_name', 'Cluster'], axis=1)
    df2 = musics[(musics['artist_name'] == selected_artist)
                 & (musics['track_name'] == selected_music)]
    df2 = df2[['tempo', 'popularity', 'energy', 'danceability',
               'valence', 'liveness', 'loudness', 'speechiness']]

    labels = list(df2)[:]
    features = df2.mean().tolist()
    features_all = df1.mean().tolist()

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    print(features_all)
    print(angles)
    fig = plt.figure(figsize=(18, 18))

    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, features, 'o-', linewidth=2,
            label="User Song", color='blue')
    ax.fill(angles, features, alpha=0.25, facecolor='blue')
    ax.set_thetagrids(angles * 180/np.pi, labels, fontsize=13)

    ax.set_rlabel_position(250)
    plt.yticks([0.25, 0.5, 0.75, 1.0, 1.25,  1.5, 1.75, 2.0], [
        "0.25", '0.5', "0.75", "1.0", "1.25", "1.5", '1.75', '2.0'], size=12)
    plt.ylim(-1.5, 1.5)

    ax.plot(angles, features_all, 'o-', linewidth=2,
            label="Recommended songs", color='orange')
    ax.fill(angles, features_all, alpha=0.25, facecolor='orange')
    ax.set_title('Mean Values')
    ax.grid(True)

    plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
    if 'compare.png' in os.listdir():
        os.remove('compare.png')
    plt.savefig('compare.png')
    im = Image.open('compare.png')
    st.write(func.playlist_song(selected_music, selected_artist, df))
    st.image(im, width=None)
