#!/usr/bin/python
from netrequest import NeteaseRequest
from lyric_parser import LyricParser


if __name__ == '__main__':
    netease_req = NeteaseRequest()
    original_lyric, transed_lyric = netease_req.get_lyrics()
    parser = LyricParser(original_lyric, transed_lyric)
    lyric_dict = parser.parse()
    for value in lyric_dict.values():
        print(value)
