from functools import reduce

import dbus
import requests

from spotifydbus import SpotifyDBus


class NeteaseRequest(object):
    """Request Netease Music API get song's lyric.

    Netease Music API github url:
        https://github.com/Binaryify/NeteaseCloudMusicApi

    You need to setup a local api server.
    """
    def __init__(self):
        """Init Netease API server."""
        self.host = '127.0.0.1'
        self.port = '3000'
        self.search_url = '/search'
        self.lyric_url = '/lyric'

    def get_song_id(self, keywords):
        """Request to get song's id."""
        url = 'http://' + self.host + ':' + self.port + self.search_url
        params = {'keywords': keywords, 'limit': 1}
        response = requests.get(url, params=params).json()
        if response['result']['songCount'] == 0:
            return None
        return response['result']['songs'][0]['id']

    def get_lyrics(self, keywords):
        """Request to get lyrics.

        :returns original lyric & Chinse translated lyric(if have).
        """
        song_id = self.get_song_id(keywords)
        if song_id is None:
            return None, None
        url = 'http://' + self.host + ':' + self.port + self.lyric_url
        params = {'id': song_id}
        response = requests.get(url, params=params).json()
        lyric_ori = response['lrc']['lyric'] if 'lrc' in response and 'lyric' in response['lrc'] else None
        lyric_trans = response['tlyric']['lyric'] if 'tlyric' in response and 'lyric' in response['tlyric'] else None
        return lyric_ori, lyric_trans
