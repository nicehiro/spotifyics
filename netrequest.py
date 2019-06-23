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

    def get_keywords(self):
        """Pick keywords from DBus."""
        spfydbus = SpotifyDBus()
        metadata = spfydbus.get_metadata()
        title = metadata[dbus.String(spfydbus.metadata_title)][:]
        album = metadata[dbus.String(spfydbus.metadata_album)][:]
        artist = reduce(lambda x, y: x[:] + ' ' + y[:],
                        metadata[dbus.String(spfydbus.metadata_artist)][:])[:]
        return '%s %s %s' % (title, album, artist)

    def get_song_id(self):
        """Request to get song's id."""
        keywords = self.get_keywords()
        url = 'http://' + self.host + ':' + self.port + self.search_url
        params = {'keywords': keywords, 'limit': 1}
        response = requests.get(url, params=params).json()
        return response['result']['songs'][0]['id']

    def get_lyrics(self):
        """Request to get lyrics.

        :returns original lyric & Chinse translated lyric(if have).
        """
        song_id = self.get_song_id()
        url = 'http://' + self.host + ':' + self.port + self.lyric_url
        params = {'id': song_id}
        response = requests.get(url, params=params).json()
        return response['lrc']['lyric'], response['tlyric']['lyric']
