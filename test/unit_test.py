import os
import unittest

import setting.setting
from rule.rules import match_bd_subtitle_auto, match_bd_subtitle_force_by_order_and_num, \
    match_bd_subtitle_force_by_subtitle, match_media_subtitle_auto, move_bd_to_target_force_by_num, \
    move_bd_to_target_force_by_each, translate_subtitles, match_media_subtitles, match_bd_subtitles
from tools.file_tool import move_media_subtitle_to_new_path, add_subtitle_for_media
from tools.match_tool import parse_names, scanning_subtitle, search_bd, scanning_media
from utils.file_util import search_maxsize_file, get_file_extension, generate_filename, get_file_name
from utils.match_util import count_most_char_by_index, search_max_prefix_suffix


class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        setting.setting.virtual_file = True
        # setting.setting.verbosity = True
        # setting.setting.debug = True
        super().__init__(*args, *kwargs)

    # 测试获取文件名及 后缀
    def test_get_file_name_and_extension(self):
        for file_path in [r"./media/200_media.text", "../fff.jpg", "../ff.jpg.tmp", ".slef", "lsef"]:
            print(get_file_name(file_path), get_file_extension(file_path))
            self.assertEqual(os.path.basename(file_path), ".".join(
                [item for item in [get_file_name(file_path), get_file_extension(file_path)] if len(item) > 0]))

    # 测试生成文件名
    def test_generate_file_name(self):
        for i in range(1, 101):
            print(generate_filename(100, "第", "集", i))
        print(generate_filename(20, "第", "集", "ova"))
        self.assertEqual(True, True)

    # 测试找出最大文件
    def test_file_util_max_file(self):
        print(setting.setting.virtual_file)
        filelist = search_maxsize_file(3, r"../test_file/bdmv/6_12/BOX1/VOL1/BDMV/STREAM", "m2ts")
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
        expect = "{'01': ['s101[m2]'], '02': ['s102[m2]'], '03': ['s103[m2]'], '04': ['s104[m2]']," + \
                 " '05': ['s105[m2]'], '06': ['s106[m2]'], '07': ['s107[m2]'], '08': ['s108[m2]']," + \
                 " '09': ['s109[m2]'], '10': ['s110[m2]']}"
        self.assertEqual(expect, str(parse_names(*name_list)))

    # 测试扫描字幕文件
    def test_scanning_subtitle(self):
        self.assertEqual(12, len(scanning_subtitle(r"../test_file/subtitle/6_12_subtitle")))

    # 测试识别媒体文件
    def test_scanning_media(self):
        self.assertEqual(200, len(scanning_media(r"../test_file/media/200_media")))

        # 测试搜索原盘目录

    def test_search_bd(self):
        self.assertEqual(6, len(search_bd(r"../test_file/bdmv/6_12")))

    def test_add_subtitle_for_media(self):
        subtitle_dic = scanning_subtitle(r"../test_file/subtitle/200_subtitle")
        print(len(subtitle_dic))
        media_dic = scanning_media(r"../test_file/media/200_media")
        print(len(media_dic))
        media_subtitle_dic, media_list = match_media_subtitle_auto(media_dic, subtitle_dic)
        self.assertEqual(200, len(media_subtitle_dic))
        # self.assertEqual(200, add_subtitle_for_media(media_subtitle_dic, only_show=False))
        self.assertEqual(201, add_subtitle_for_media(media_subtitle_dic, only_show=True))

    # 测试自动模式添加原盘字幕
    def test_add_subtitle_for_BDMV_auto(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(r"../test_file/subtitle/6_12_subtitle")
        media_subtitle_dic, media_list = match_bd_subtitle_auto(subtitle_dic, r"../test_file/bdmv/6_12")
        self.assertEqual(12, len(media_subtitle_dic))
        self.assertEqual(12, add_subtitle_for_media(media_subtitle_dic, only_show=True))

    # 测试自动模式添加原盘字幕
    def test_add_subtitle_for_BDMV_force_each(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(r"../test_file/subtitle/6_11_subtitle")
        media_subtitle_dic, media_list = match_bd_subtitle_force_by_order_and_num(subtitle_dic, 2,
                                                                                  r"../test_file/bdmv/6_11")
        self.assertEqual(11, len(media_subtitle_dic))
        self.assertEqual(11, add_subtitle_for_media(media_subtitle_dic, only_show=True))

    # 测试强制顺序模式添加原盘字幕
    def test_add_subtitle_for_BDMV_force_order(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(r"../test_file/subtitle/7_12_subtitle")
        media_subtitle_dic, media_list = match_bd_subtitle_force_by_order_and_num(subtitle_dic, 2,
                                                                                  r"../test_file/bdmv/6_12")
        self.assertEqual(12, len(media_subtitle_dic))
        self.assertEqual(24, add_subtitle_for_media(media_subtitle_dic, only_show=True))

    # 测试强制匹配
    def test_match_bd_subtitle_force_by_subtitle(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(r"../test_file/subtitle/8_25_subtitle")
        media_subtitle_dic, media_list = match_bd_subtitle_force_by_subtitle(subtitle_dic, False,
                                                                             r"../test_file/bdmv/8_25")
        self.assertEqual(25, len(media_subtitle_dic))
        self.assertEqual(50, add_subtitle_for_media(media_subtitle_dic, only_show=True))

    # 促成翻转强制匹配
    def test_match_bd_subtitle_force_by_subtitle_reverse(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(r"../test_file/subtitle/6_13_subtitle")
        media_subtitle_dic, media_list = match_bd_subtitle_force_by_subtitle(subtitle_dic, True,
                                                                             r"../test_file/bdmv/6_13_rev")
        self.assertEqual(13, len(media_subtitle_dic))
        self.assertEqual(13, add_subtitle_for_media(media_subtitle_dic, only_show=True))

    # 测试文件移动
    def test_move_media_subtitle_to_new_path(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(r"../test_file/subtitle/6_12_subtitle")
        media_subtitle_dic, media_list = match_bd_subtitle_auto(subtitle_dic, r"../test_file/bdmv/6_12")
        self.assertEqual(12, len(media_subtitle_dic))
        self.assertEqual(12, move_media_subtitle_to_new_path(media_subtitle_dic,
                                                             {order + 1: media_list[order] for order in
                                                              range(len(media_list))},
                                                             r"../test_file/target/bd_target",
                                                             "第", "集", only_show=True))

    # 命令方法测试
    # 测试翻译
    def test_translate(self):
        s = r"../test_file/subtitle/6_12_subtitle"
        t = r"../test_file/subtitle/6_12_subtitle_translated"
        self.assertEqual(12, translate_subtitles(s, t, "../rule.csv"))

    # 测试根据数量移动
    def test_move_bd_to_target_force_by_num(self):
        self.assertEqual(12,
                         move_bd_to_target_force_by_num(r"../test_file/target/bd_target2", "第", "集", 12, True, False,
                                                        r"../test_file/bdmv/6_12"))
        self.assertEqual(25,
                         move_bd_to_target_force_by_num(r"../test_file/target/bd_target3", "第", "集", 25, True, False,
                                                        r"../test_file/bdmv/8_25"))

    # 指定数量跟每个光盘文件移动
    def test_move_bd_to_target_force_by_each(self):
        self.assertEqual(12, move_bd_to_target_force_by_each(r"../test_file/target/bd_target4", "第", "集", 12, 2, True,
                                                             r"../test_file/bdmv/7_12"))

    # 原盘统一测试
    def test_match_bd_subtitles(self):
        self.assertEqual(12, match_bd_subtitles(r"../test_file/subtitle/6_12_subtitle", None, None, None, None, False,
                                                False, True, False, "../test_file/bdmv/6_12"))
        self.assertEqual(24,
                         match_bd_subtitles(r"../test_file/subtitle/7_12_subtitle", None, None, None, 2, True, False,
                                            True, False, "../test_file/bdmv/7_12"))
        self.assertEqual(50,
                         match_bd_subtitles(r"../test_file/subtitle/8_25_subtitle", None, None, None, None, True, False,
                                            True, False, "../test_file/bdmv/8_25"))
        self.assertEqual(12,
                         match_bd_subtitles(r"../test_file/subtitle/6_12_subtitle", r"../test_file/target/bd_target1",
                                            "第", "集", None, False, True,
                                            True, False, "../test_file/bdmv/6_12"))
        self.assertEqual(12,
                         match_bd_subtitles(r"../test_file/subtitle/7_12_subtitle", r"../test_file/target/bd_target2",
                                            "第", "集", 2, True, True,
                                            True, False, "../test_file/bdmv/7_12"))
        self.assertEqual(25,
                         match_bd_subtitles(r"../test_file/subtitle/8_25_subtitle", r"../test_file/target/bd_target3",
                                            "第", "集", None, True, True,
                                            True, False, "../test_file/bdmv/8_25"))
        self.assertEqual(13,
                         match_bd_subtitles(r"../test_file/subtitle/6_13_subtitle", r"../test_file/target/bd_target1",
                                            "第", "集", None, True, True,
                                            True, True, "../test_file/bdmv/6_13_rev"))
    # 媒体统一测试
    def test_match_media_subtitles(self):
        self.assertEqual(201,
                         match_media_subtitles(r"../test_file/media/200_media", r"../test_file/subtitle/200_subtitle",
                                               None, None, None, True, True))
        self.assertEqual(200,
                         match_media_subtitles(r"../test_file/media/200_media", r"../test_file/subtitle/200_subtitle",
                                               r"../test_file/target/bd_target", None, "集", True, True))


if __name__ == '__main__':
    unittest.main()
