import os
from src.music_utils.Song import Playlist, Song


def create_all_music_playlist():
    my_playlist = Playlist(name="All Songs")
    PATH_TO_MUSIC_LIB = os.path.join(os.getcwd(), r'music_utils\music_lib')
    for file in os.listdir(PATH_TO_MUSIC_LIB):
        if file.endswith(".mp3"):
            my_playlist.songs.append(Song(os.path.join(PATH_TO_MUSIC_LIB, file)))

    return my_playlist


def create_downloaded_music_playlist():
    my_playlist = Playlist(name="My Songs")
    PATH_TO_MUSIC_LIB = os.path.join(os.getcwd(), r'music_utils\music_lib')
    for file in os.listdir(PATH_TO_MUSIC_LIB):
        if file.endswith(".mp3"):
            my_playlist.songs.append(Song(os.path.join(PATH_TO_MUSIC_LIB, file)))

    return my_playlist


class PlaylistHandler:
    def __init__(self):
        self.all_music = create_all_music_playlist()
        self.my_music = create_downloaded_music_playlist()