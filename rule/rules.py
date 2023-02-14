import os
import re

from setting import setting
from tools.file_tool import add_subtitle_for_media, move_media_subtitle_to_new_path, move_copy_files
from tools.match_tool import scanning_subtitle, search_bd, match_bd_media, match_bd_media_force_each, \
    match_bd_media_force_dynamic, scanning_media
from tools.translate_tool import init_translate_dic, translate_file
from utils.file_util import get_file_extension, generate_filename

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
def match_bd_subtitle_auto(subtitle_dic: dict, *BDMV_path: str) -> (dict, list):
    # # 搜索字幕目录
    # subtitle_dic = scanning_subtitle(subtitles_dir)
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    print(dic_list)
    # subtitle_dic, dic_list = search_bdmv_and_subtitles(BDMV_path, subtitles_dir)
    # dic_list = search_bdmv_and_subtitles(BDMV_path, subtitles_dir)
    for name, rule in KEY_WORDS_RULE_DIC.items():
        keywords = sorted([keyword for keyword in subtitle_dic.keys() if rule.match(keyword)])
        print("采用 《{}》 规则解析字幕 共{}集\n分别为\t{}".format(name, len(keywords), "\t".join(keywords)))
        # 尝试根据字幕数量完全匹配
        media_list = match_bd_media(len(keywords), *dic_list)
        if len(media_list) > 0:
            return _match_media_subtitle(subtitle_dic, media_list, *keywords), media_list
    print("匹配失败")
    return {}, []


# 原盘剧集匹配
# 指定每盘数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_order_and_num(subtitle_dic: dict, each: int, *BDMV_path: str) -> (dict, list):
    # # 搜索字幕目录
    # subtitle_dic = scanning_subtitle(subtitles_dir)
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    # 尝试根据字幕数量强制匹配
    media_list = match_bd_media_force_each(len(subtitle_dic), each, *dic_list)
    if len(media_list) > 0:
        return _match_media_subtitle(subtitle_dic, media_list, *sorted(subtitle_dic.keys())), media_list
    print("匹配失败")
    return {}, []


# 原盘剧集匹配
# 指定标题数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_subtitle(subtitle_dic: dict, *BDMV_path: str) -> (dict, list):
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
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
            orders.append(order)
    return media_subtitle_dic, [order_media_dic[order] for order in sorted(orders)]


"""
由控制台直接调用
"""


# 翻译字幕
def translate_subtitles(subtitles_path: str, target_path: str, translate_dic: str = "./rule.csv") -> int:
    result = 0
    init_translate_dic(translate_dic)
    # 目标路径初始化
    if target_path is None:
        target_path = subtitles_path
    # 翻译
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


# 移动bd文件到目录路径,指定数量
def move_bd_to_target_force_by_num(target_path: str, prefix: str, suffix: str, num: int, only_show: bool,
                                   *BDMV_path: str) -> int:
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    # 计算数量
    avg_num = round(num / len(dic_list))
    media_list = match_bd_media_force_dynamic(num, avg_num, *dic_list)
    order_media_dic = {order + 1: media_list[order] for order in range(len(media_list))}
    source_target_dic = {}
    for order, media_path in order_media_dic.items():
        new_filename = generate_filename(num, prefix, suffix, order) + "." + get_file_extension(media_path)
        source_target_dic[media_path] = os.path.join(target_path, new_filename)

    succeed, error = move_copy_files(source_target_dic, only_show)
    return succeed


# 移动bd文件到目录路径,指定数量
def move_bd_to_target_force_by_each(target_path: str, prefix: str, suffix: str, num: int, each: int, only_show: bool,
                                    *BDMV_path: str) -> int:
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    if num is None:
        num = len(dic_list) * each
    media_list = match_bd_media_force_each(num, each, *dic_list)
    order_media_dic = {order + 1: media_list[order] for order in range(len(media_list))}
    source_target_dic = {}
    for order, media_path in order_media_dic.items():
        new_filename = generate_filename(num, prefix, suffix, order) + "." + get_file_extension(
            media_path)
        source_target_dic[media_path] = os.path.join(target_path, new_filename)

    succeed, error = move_copy_files(source_target_dic, only_show)
    return succeed


# 原盘字幕匹配
def match_bd_subtitles(subtitle_path: str, target_path: str, prefix: str, suffix: str, each: int,
                       force: bool, only_show: bool, copy_subtitle: bool,
                       *bd_path) -> int:
    # print(subtitle_path, target_path, prefix, suffix, each, force, only_show, copy_subtitle, bd_path)
    subtitle_dic = scanning_subtitle(subtitle_path)
    if len(subtitle_dic) == 0:
        print("匹配字幕失败")
        return 0
    if not force:
        media_subtitle_dic, media_list = match_bd_subtitle_auto(subtitle_dic, *bd_path)
    else:
        if each is not None:
            # 根据字幕数量和每个光盘文件中有效媒体的数量匹配
            media_subtitle_dic, media_list = match_bd_subtitle_force_by_order_and_num(subtitle_dic, each, *bd_path)
        else:
            # 仅根据字幕数量强制匹配
            media_subtitle_dic, media_list = match_bd_subtitle_force_by_subtitle(subtitle_dic, *bd_path)
    if len(media_subtitle_dic) == 0:
        print("匹配字幕和媒体文件失败")
        return 0
    if target_path is None:
        return add_subtitle_for_media(media_subtitle_dic, only_show=True)
    else:
        return move_media_subtitle_to_new_path(media_subtitle_dic=media_subtitle_dic,
                                               order_media_dic={order + 1: media_list[order] for order in
                                                                range(len(media_list))},
                                               target_dir=target_path, suffix=prefix, prefix=suffix,
                                               only_show=only_show, copy_subtitle=copy_subtitle)


# 匹配媒体文件和字幕
def match_media_subtitles(media_path: str, subtitle_path: str, target_path: str, prefix: str, suffix: str,
                          only_show: bool, copy_subtitle: bool) -> int:
    print(only_show)
    subtitle_dic = scanning_subtitle(subtitle_path)
    media_dic = scanning_media(media_path)
    if setting.debug:
        print("subtitle_dic :", subtitle_dic)
        print("media_dic :", media_dic)
    if len(media_dic) == 0 or len(subtitle_dic) == 0:
        print("匹配异常,共匹配到字幕{}个,共匹配到媒体文件{}个".format(len(subtitle_dic), len(media_dic)))
        return 0
    # 匹配
    media_subtitle_dic, media_list = match_media_subtitle_auto(media_dic, subtitle_dic)
    if len(media_subtitle_dic) == 0:
        print("匹配失败")
    if target_path is None:
        return add_subtitle_for_media(media_subtitle_dic=media_subtitle_dic, only_show=only_show,
                                      copy_subtitle=copy_subtitle)
    else:
        return move_media_subtitle_to_new_path(media_subtitle_dic=media_subtitle_dic,
                                               order_media_dic={order + 1: media_list[order] for order in
                                                                range(len(media_list))},
                                               target_dir=target_path, suffix=prefix, prefix=suffix,
                                               only_show=only_show, copy_subtitle=copy_subtitle)
