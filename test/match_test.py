import shutil
import unittest

from rule.rules import match_bd_caption_force_by_caption
from tools.file_tool import add_caption_for_media, move_media_caption_to_new_path
from tools.match_tool import scanning_captions, search_bd


class MyTestCase(unittest.TestCase):
    def test_move(self):
        source = r"H:\videos\为美好的世界献上祝福1\为美好的世界献上祝福S01N01.m2ts"
        # target =r"H:\videos\素晴1\为美好的世界献上祝福S01N01.m2ts"
        target = r"H:\videos\素晴1\Konosuba God's Blessing on this Wonderful World! vol.1\BDROM\BDMV\STREAM\00004.m2ts"
        # shutil.move(source, target)
        # shutil.move(target,source)

    def test_match_bd_caption_force_by_caption(self):
        # # 搜索字幕目录
        caption_dic = scanning_captions(
            r"H:\字幕\素晴\[VCB-Studio] Kono Subarashii Sekai ni Shukufuku wo! [Ma10p_1080p]")
        media_caption_dic, media_list = match_bd_caption_force_by_caption(
            r"H:\videos\素晴1",
            caption_dic)
        self.assertEqual(11, len(media_caption_dic))
        self.assertEqual(11, move_media_caption_to_new_path(media_caption_dic,
                                                             {order + 1: media_list[order] for order in
                                                              range(len(media_list))},
                                                             r"H:\videos\为美好的世界献上祝福1",
                                                             "为美好的世界献上祝福S01N", "", only_show=True))
        # (media_caption_dic, only_show=False))

    def test_match_bd_caption_forceTrue_by_caption2(self):
        # 搜索字幕目录
        caption_dic = scanning_captions(
            r"H:\字幕\素晴\[VCB-Studio] Kono Subarashii Sekai ni Shukufuku wo! 2 [Ma10p_1080p]", )
        media_caption_dic ,media_list= match_bd_caption_force_by_caption(
            r"H:\videos\素晴2",
            caption_dic)
        print(media_caption_dic)
        self.assertEqual(11, len(media_caption_dic))
        # self.assertEqual(11, add_caption_for_media(media_caption_dic, only_show=True))
        self.assertEqual(11, move_media_caption_to_new_path(media_caption_dic,
                                                            {order + 1: media_list[order] for order in
                                                             range(len(media_list))},
                                                            r"H:\videos\为美好的世界献上祝福2",
                                                            "为美好的世界献上祝福S02N", "", only_show=False))

    # 测试搜索原盘目录
    def test_search_bd(self):
        bd_paths = search_bd(r"H:\media\[BDMV] Konosuba God's Blessing on this Wonderful World!")
        print(bd_paths)
        self.assertEqual(6, len(bd_paths))


if __name__ == '__main__':
    unittest.main()
