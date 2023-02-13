import shutil
import unittest

from rule.rules import match_bd_subtitle_force_by_subtitle, match_bd_subtitle_auto, match_media_subtitle_auto
from tools.file_tool import add_subtitle_for_media, move_media_subtitle_to_new_path
from tools.match_tool import scanning_subtitle, search_bd, scanning_media


class MyTestCase(unittest.TestCase):


    def test_move(self):
        source = r"H:\videos\为美好的世界献上祝福1\为美好的世界献上祝福S01N01.m2ts"
        # target =r"H:\videos\素晴1\为美好的世界献上祝福S01N01.m2ts"
        target = r"H:\videos\素晴1\Konosuba God's Blessing on this Wonderful World! vol.1\BDROM\BDMV\STREAM\00004.m2ts"
        shutil.move(source, target)
        # shutil.move(target,source)

    def test_match_bd_subtitle_force(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(r"H:\字幕\[SweetSub][DARLING in the FRANXX][BDrip][CHS&CHT]\chs")
        media_subtitle_dic, media_list = match_bd_subtitle_force_by_subtitle(
            r"H:\videos\Darling in the Franxx",
            subtitle_dic)
        self.assertEqual(24, len(media_subtitle_dic))
        self.assertEqual(24, move_media_subtitle_to_new_path(media_subtitle_dic,
                                                             {order + 1: media_list[order] for order in
                                                              range(len(media_list))},
                                                             r"H:\videos\比翼之吻",
                                                             "比翼之吻第", "话", only_show=False))

    def test_match_media_subtitle_force(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(r"H:\字幕\[魔卡少女樱][Cardcaptor Sakura][カードキャプターさくら][BDRip][TV 01-70 Fin][chs+cht][ssa][LITEN SAKURA制作小组简繁][修正]")
        print(subtitle_dic)
        media_dic = scanning_media(r"H:\videos\[アニメ BD][カードキャプターさくら][lloup][Cardcaptor_Sakura][BDrip][01-70]")
        print(media_dic)
        media_subtitle_dic, media_list = match_media_subtitle_auto(media_dic, subtitle_dic)
        self.assertEqual(70, len(media_subtitle_dic))
        self.assertEqual(70, add_subtitle_for_media(media_subtitle_dic, only_show=False))



    def test_match_bd_subtitle_force_by_subtitle(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(
            r"H:\字幕\素晴\[VCB-Studio] Kono Subarashii Sekai ni Shukufuku wo! [Ma10p_1080p]")
        media_subtitle_dic, media_list = match_bd_subtitle_force_by_subtitle(
            r"H:\videos\素晴1",
            subtitle_dic)
        self.assertEqual(11, len(media_subtitle_dic))
        self.assertEqual(11, move_media_subtitle_to_new_path(media_subtitle_dic,
                                                             {order + 1: media_list[order] for order in
                                                              range(len(media_list))},
                                                             r"H:\videos\为美好的世界献上祝福1",
                                                             "为美好的世界献上祝福S01N", "", only_show=False))
        # (media_subtitle_dic, only_show=False))

    def test_match_bd_subtitle_force_by_subtitle2(self):
        # # 搜索字幕目录
        subtitle_dic = scanning_subtitle(
            r"H:\字幕\素晴\[VCB-Studio] Kono Subarashii Sekai ni Shukufuku wo! 2 [Ma10p_1080p]", )
        media_subtitle_dic = match_bd_subtitle_force_by_subtitle(
            r"H:\media\[BDMV][Kono Subarashii Sekai ni Shukufuku wo ! 2][Vol.1-Vol.5+OVA Fin]",
            subtitle_dic)
        self.assertEqual(11, len(media_subtitle_dic))
        self.assertEqual(11, add_subtitle_for_media(media_subtitle_dic, only_show=False))

    # 测试搜索原盘目录
    def test_search_bd(self):
        bd_paths = search_bd(r"H:\media\[BDMV] Konosuba God's Blessing on this Wonderful World!")
        print(bd_paths)
        self.assertEqual(6, len(bd_paths))


if __name__ == '__main__':
    unittest.main()
