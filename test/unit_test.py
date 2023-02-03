import unittest

from rule.rules import match_bd_subtitle_auto, match_bd_subtitle_force_by_order
from tools.match_tool import parse_names, scanning_subtitle, search_bd, add_subtitle_for_metia
from utils.file_util import search_maxsize_file
from utils.match_util import count_most_char_by_index, search_max_prefix_suffix


class MyTestCase(unittest.TestCase):
    # 测试找出最大文件
    def test_file_util_max_file(self):
        filelist = search_maxsize_file(3,
                                       r"D:\Downloads\fff\BD\[BDMV]ゼロから始める魔法の書 BDBOX1-2 Fin\BOX1\VOL1\BDMV\STREAM",
                                       "m2ts")
        self.assertEqual("['00003.m2ts', '00004.m2ts', '00005.m2ts']", str(filelist))  # add assertion here

    # 测试搜寻索引所在位置最多的字符
    def test_count_most_char_by_index(self):
        c = count_most_char_by_index(2, "abc", "abd", "ccc", "dec", "inc", "ffc")
        self.assertEqual("c", c)

    # 测试搜索最大公共前缀后缀
    def test_search_max_prefix_suffix(self):
        name_list = ["s101[m2]", "s102[m2]", "s103[m2]", "s104[m2]", "s105[m2]", "s106[m2]", "s107[m2]", "s108[m2]",
                     "s109[m2]", "s110[m2]"]
        name_list2 = ["s101[m2]", "s102[m2]", "s103[m2]", "s104[m2]", "s105[m2]", "s106[m2]", "s107[m2]", "s108[m2]",
                      "s109[m4]", "s110[m4]"]

        pf, sf = search_max_prefix_suffix(*name_list)
        pf2, sf2 = search_max_prefix_suffix(*name_list2)
        self.assertEqual("s1 [m2]", pf + " " + sf)
        self.assertEqual("s1 ]", pf2 + " " + sf2)
        pf, sf = search_max_prefix_suffix(*name_list, ratio=0.8)
        pf2, sf2 = search_max_prefix_suffix(*name_list2, ratio=0.8)
        self.assertEqual("s10 [m2]", pf + " " + sf)
        self.assertEqual("s10 [m2]", pf2 + " " + sf2)

    # 测试名称匹配
    def test_match_by_rule(self):
        name_list = ["s101[m2]", "s102[m2]", "s103[m2]", "s104[m2]", "s105[m2]", "s106[m2]", "s107[m2]", "s108[m2]",
                     "s109[m2]", "s110[m2]"]
        expect = """{'01': ['s101[m2]'], '02': ['s102[m2]'], '03': ['s103[m2]'], '04': ['s104[m2]'], '05': ['s105[m2]'], '06': ['s106[m2]'], '07': ['s107[m2]'], '08': ['s108[m2]'], '09': ['s109[m2]'], '10': ['s110[m2]']}"""
        self.assertEqual(expect, str(parse_names(*name_list)))

    # 测试扫描字幕文件
    def test_scanning_subtitle(self):
        self.assertEqual(12, len(scanning_subtitle(r"D:\Downloads\tc")))

    # 测试搜索原盘目录
    def test_search_bd(self):
        self.assertEqual(6, len(search_bd(r"D:\Downloads\fff\BD\[BDMV]ゼロから始める魔法の書 BDBOX1-2 Fin")))

    # 测试自动模式添加原盘字幕
    def test_add_subtitle_for_BDMV_auto(self):
        metia_subtitle_dic = match_bd_subtitle_auto(r"D:\Downloads\fff\BD\[BDMV]ゼロから始める魔法の書 BDBOX1-2 Fin",
                                                    r"D:\Downloads\tc")
        self.assertEqual(12, len(metia_subtitle_dic))
        self.assertEqual(12, add_subtitle_for_metia(metia_subtitle_dic, only_show=True))

    # 测试强制顺序模式添加原盘字幕
    def test_add_subtitle_for_BDMV_force_order(self):
        metia_subtitle_dic = match_bd_subtitle_force_by_order(
            r"D:\Downloads\fff\BD\[BDMV][Kyoukai no Kanata][Vol.01-07]",
            r"D:\Downloads\fff\字幕\[VCB-Studio&Liuyun] Kyokai no Kanata [Hi10p_1080p]"
            , 2)
        self.assertEqual(12, len(metia_subtitle_dic))
        self.assertEqual(12, add_subtitle_for_metia(metia_subtitle_dic, only_show=True))


if __name__ == '__main__':
    unittest.main()
