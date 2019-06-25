import re
from collections import OrderedDict


class LyricParser(object):
    """Parse Netease Mysic API lyric."""

    def __init__(self, has_trans=True):
        self.pattern = re.compile('\[(\d+):(\d+).(\d+)\](.*)\n')
        self.has_trans = has_trans

    def parse2dict(self, lyric):
        """Parse lyrics json file to Dict.

        :return dict
            key: millseconds of lyric position
            value: lyric
        """
        lyric_list = self.pattern.findall(lyric)
        d = OrderedDict()
        for line in lyric_list:
            mills = int(line[0]) * 60 * 1000 + int(line[1]) * 1000 + int(line[2])
            txt = line[3]
            d[mills] = txt
        return d

    def parse(self, lyric_origin, lyric_translate):
        """
        Concat original lyric with translated lyric.

        :param lyric_origin: original lyric
        :param lyric_translate: translated lyric
        :return: dict
            key: millseconds of lyric position
            value: lyric
        """
        lyric_transed_dict = OrderedDict()
        if self.has_trans and lyric_translate:
            lyric_transed_dict = self.parse2dict(lyric_translate)
        lyric_ori_dict = None
        if lyric_origin:
            lyric_ori_dict = self.parse2dict(lyric_origin)
            for key in lyric_ori_dict:
                lyric_ori_dict[key] += '\n' + lyric_transed_dict[key] + '\n' \
                    if key in lyric_transed_dict else '\n'
        return lyric_ori_dict
