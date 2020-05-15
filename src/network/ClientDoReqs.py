from src.music_utils.Song import Playlist
from src.network.NetworkCommunication import *
from src.network.OperationType import OperationType

server_songs = Playlist()
socket = None
log = None


def init(sock, logger):
    global socket
    socket = sock
    global log
    log = logger


def do_req(req, socket, log):
    pass


def get_all_server_songs(server_msg_raw):
    server_msg_raw = server_msg_raw[len(OperationType.ALL_SONGS.name) + len(SEPARATOR_CHAR) + 1: len(server_msg_raw) - 2]
    server_msg_raw = server_msg_raw.replace("'", "")

    global server_songs
    server_songs.conv_to_obj(playlist=server_msg_raw.split(","), name="ServerAllSongs")


def search_song(search):
    send_req(assemble_req(OperationType.SEARCH.name, search), socket, log)