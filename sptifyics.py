#!/usr/bin/python
from netrequest import NeteaseRequest
from lyric_parser import LyricParser


if __name__ == '__main__':
    netease_req = NeteaseRequest()
    original_lyric, transed_lyric = netease_req.get_lyrics()
    parser = LyricParser()
    lyric_dict = parser.parse(original_lyric, transed_lyric)
    if lyric_dict:
        for value in lyric_dict.values():
            print(value)
