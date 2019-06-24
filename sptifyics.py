#!/usr/bin/python
from netrequest import NeteaseRequest


if __name__ == '__main__':
    netease_req = NeteaseRequest()
    original_lyric, transed_lyric = netease_req.get_lyrics()
    print(original_lyric, transed_lyric)
