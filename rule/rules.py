import os
import re

from setting import setting
from tools.match_tool import scanning_subtitle, search_bd, match_bd_media, match_bd_media_force, \
    match_bd_media_force_dynamic
from tools.translate_tool import init_translate_dic, translate_file

KEY_WORDS_RULE_DIC = {
    "全部匹配": re.compile(r"^.*$"),
    "数字及OVA,PV": re.compile(r"^\d+|OVA|PV$"),
    "数字及.5": re.compile(r"^\d+(\.5)?$"),
    "纯数字": re.compile(r"^\d+$"),
}


# 公共方法
# 字幕与媒体配对
def _match_media_subtitle(subtitle_dic: dict, media_list: list, *keywords) -> dict:
    result = {}
    for index in range(len(media_list)):
        result[media_list[index]] = subtitle_dic[keywords[index]]

    if setting.verbosity:
        for index in range(len(media_list)):
            print("剧集：\t{}\n媒体：\t{}".format(keywords[index], media_list[index]))
            print("字幕：\t{}\n".format("\n\t\t".join(subtitle_dic[keywords[index]])))
    return result


# 原盘剧集匹配
# 根据字幕动态匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_auto(BDMV_path: str, subtitle_dic: dict) -> (dict, list):
    # # 搜索字幕目录
    # subtitle_dic = scanning_subtitle(subtitles_dir)
    # 搜索原盘目录
    dic_list = search_bd(BDMV_path)
    # subtitle_dic, dic_list = search_bdmv_and_subtitles(BDMV_path, subtitles_dir)
    # dic_list = search_bdmv_and_subtitles(BDMV_path, subtitles_dir)
    for name, rule in KEY_WORDS_RULE_DIC.items():
        keywords = sorted([keyword for keyword in subtitle_dic.keys() if rule.match(keyword)])
        print("采用 {} 规则解析字幕 共{}集\n分别为\t{}".format(name, len(keywords), "\t".join(keywords)))
        # 尝试根据字幕数量完全匹配
        media_list = match_bd_media(len(keywords), *dic_list)
        if len(media_list) > 0:
            return _match_media_subtitle(subtitle_dic, media_list, *keywords), media_list
    print("匹配失败")
    return {}, []


# 原盘剧集匹配
# 指定每盘数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_order_and_num(BDMV_path: str, subtitle_dic: dict, per_number: int) -> (dict, list):
    # # 搜索字幕目录
    # subtitle_dic = scanning_subtitle(subtitles_dir)
    # 搜索原盘目录
    dic_list = search_bd(BDMV_path)
    # 尝试根据字幕数量强制匹配
    media_list = match_bd_media_force(len(subtitle_dic), per_number, *dic_list)
    if len(media_list) > 0:
        return _match_media_subtitle(subtitle_dic, media_list, *sorted(subtitle_dic.keys())), media_list
    print("匹配失败")
    return {}, []


# 原盘剧集匹配
# 指定每盘数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_subtitle(BDMV_path: str, subtitle_dic: dict) -> (dict, list):
    # 搜索原盘目录
    dic_list = search_bd(BDMV_path)
    # 计算数量
    avg_num = round(len(subtitle_dic) / len(dic_list))
    media_list = match_bd_media_force_dynamic(len(subtitle_dic), avg_num, *dic_list)
    if len(media_list) > 0:
        return _match_media_subtitle(subtitle_dic, media_list, *sorted(subtitle_dic.keys())), media_list
    print("匹配失败")
    return {}, []


# 媒体文件字幕匹配 关键字
def match_media_subtitle_auto(order_media_dic: dict, order_subtitle_dic: dict) -> (dict, list):
    media_subtitle_dic, orders = {}, []
    for order, media in order_media_dic.items():
        if order in order_subtitle_dic.keys():
            media_subtitle_dic[media] = order_subtitle_dic[order]
    return media_subtitle_dic, [order_media_dic[order] for order in sorted(orders)]


# 翻译字幕
def translate_subtitles(subtitles_path: str, target_path: str, translate_dic: str = "./rule.csv") -> int:
    result = 0
    init_translate_dic(translate_dic)
    for file_name in os.listdir(subtitles_path):
        extensions = file_name[file_name.rfind(".") + 1:]
        if extensions in setting.SUPPORT_SUBLIST:
            if translate_file(os.path.join(subtitles_path, file_name), os.path.join(target_path, file_name)):
                result += 1
                if setting.verbosity:
                    print(os.path.join(subtitles_path, file_name), "翻译成功")
            else:
                print("path:", os.path.join(subtitles_path, file_name), "翻译出错")
    return result
