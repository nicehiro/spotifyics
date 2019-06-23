#!/usr/bin/python
from spotifydbus import SpotifyDBus
from netrequest import NeteaseRequest


if __name__ == '__main__':
    spfy = SpotifyDBus()
    netease_req = NeteaseRequest()
    original_lyric, transed_lyric = netease_req.get_lyrics()
    print(original_lyric, transed_lyric)
