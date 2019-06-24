import re
from collections import OrderedDict


class LyricParser(object):
    """Parse Netease Mysic API lyric."""

    def __init__(self, lyric_ori, lyric_transed, has_trans=True):
        self.pattern = re.compile('\[(\d+):(\d+).(\d+)\](.*)\n')
        self.lyric_origin = lyric_ori
        self.lyric_translate = lyric_transed
        self.has_trans = has_trans

    def parse2dict(self, lyric):
        lyric_list = self.pattern.findall(lyric)
        d = OrderedDict()
        for line in lyric_list:
            mills = int(line[0]) * 60 * 1000 + int(line[1]) * 1000 + int(line[2])
            txt = line[3]
            d[mills] = txt
        return d

    def parse(self):
        lyric_ori_dict = self.parse2dict(self.lyric_origin)
        lyric_transed_dict = OrderedDict()
        if self.has_trans and self.lyric_translate:
            lyric_transed_dict = self.parse2dict(self.lyric_translate)
        for key in lyric_ori_dict:
            lyric_ori_dict[key] += '\n' + lyric_transed_dict[key] + '\n' \
                if key in lyric_transed_dict else '\n'
        return lyric_ori_dict
