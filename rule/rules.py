import math
import os
import re

from setting import setting
from tools.file_tool import add_subtitle_for_media, move_media_subtitle_to_new_path, file_move
from tools.match_tool import scanning_subtitle, search_bd, match_bd_media_force_each, \
    match_bd_media_force_dynamic, scanning_media
from tools.translate_tool import init_translate_dic, translate_file
from utils.file_util import get_file_extension, generate_filename, get_file_size

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


# 公共方法
# 字幕与媒体配对
def _match_media_subtitle_new(subtitle_dic: dict, media_list: list, *keywords) -> (dict, dict):
    media_subtitle_dict, order_media_dict = {}, dict(zip(keywords, media_list))
    for order, media in order_media_dict.items():
        media_subtitle_dict[media] = subtitle_dic[order]
    if setting.verbosity:
        for order, media in order_media_dict.items():
            print("剧集：\t{}\n媒体：\t{}".format(order, media))
            print("字幕：\t{}\n".format("\n\t\t".join(media_subtitle_dict[media])))
    return media_subtitle_dict, order_media_dict


# 原盘剧集匹配
# 根据字幕动态匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_auto(subtitle_dic: dict, *BDMV_path: str) -> (dict, dict):
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    media_list = match_bd_file_auto(*dic_list)
    for name, rule in KEY_WORDS_RULE_DIC.items():
        keywords = sorted([keyword for keyword in subtitle_dic.keys() if rule.match(keyword)])
        print("采用 《{}》 规则解析字幕 共{}集\n分别为\t{}".format(name, len(keywords), "\t".join(keywords)))
        # 尝试根据字幕数量完全匹配
        if len(media_list) == len(keywords):
            return _match_media_subtitle_new(subtitle_dic, media_list, *keywords)
    print("匹配失败")
    return {}, []


# 原盘动态匹配
# 根据文件大小动态匹配
def match_bd_file_auto(*dic_list: str) -> list:
    result = []
    # 媒体文件列表
    media_size_dic, media_level_dic, arg_dic = {}, {}, []
    for i in range(len(dic_list)):
        media_dir = os.path.join(dic_list[i], "BDMV", "STREAM")
        media_path_list = [os.path.join(media_dir, media_name) for media_name in os.listdir(media_dir) if
                           media_name.endswith(".m2ts")]
        media_path_list.sort()
        print(media_path_list)
        for j in range(len(media_path_list)):
            media_size_dic[media_path_list[j]] = get_file_size(media_path_list[j])
            media_level_dic[media_path_list[j]] = ((i + 1) << 9) + j
    # 找出最大n集取平均值，然后求方差
    size_items = [size for size in media_size_dic.values()]
    size_items.sort()
    avg = int(sum(size_items[-setting.AVG_NUM:]) / setting.AVG_NUM)
    max_size = size_items[-1]
    # 参数列表 (媒体路径,文件大小,方差)
    arg_item = [(path, size, (size - avg) ** 2) for path, size in media_size_dic.items()]
    # 方差排序
    arg_item.sort(key=lambda item: item[2])
    for i in range(len(arg_item)):
        print(arg_item[i])
        media_path, size, variance = arg_item[i]
        print(media_path, size, variance)
        if setting.debug:
            print("mediaPath:\t{}\tsize:\t{}\tvariance:\t{}\tvisualSize:\t{:.2f}G\tvarianceLenth:\t{}"
                  .format(media_path, size, variance, size / 2 ** 30, round(math.log10(max(variance, 1)))))
        # 方差比率和文件大小比率到达指定值，跳出
        if i > 0 and max_size / size > setting.SIZE_RATE and variance / arg_item[i - 1][2] > setting.VARIANCE_RATE:
            break
        result.append(media_path)

    print("*" * 100)
    result.sort(key=lambda item: media_level_dic[item])
    if setting.verbosity:
        for media_path in result:
            print(media_path)
        print("*" * 100)
    return result


# 原盘剧集匹配
# 指定每盘数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_order_and_num(subtitle_dic: dict, each: int, *BDMV_path: str) -> (dict, dict):
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    # 尝试根据字幕数量强制匹配
    media_list = match_bd_media_force_each(len(subtitle_dic), each, *dic_list)
    if len(media_list) > 0:
        return _match_media_subtitle_new(subtitle_dic, media_list, *sorted(subtitle_dic.keys()))
    print("匹配失败")
    return {}, []


# 原盘剧集匹配
# 指定标题数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_subtitle(subtitle_dic: dict, reversal: bool, *BDMV_path: str) -> (dict, dict):
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    # 计算数量
    avg_num = round(len(subtitle_dic) / len(dic_list))
    media_list = match_bd_media_force_dynamic(len(subtitle_dic), avg_num, reversal, *dic_list)
    if len(media_list) > 0:
        return _match_media_subtitle_new(subtitle_dic, media_list, *sorted(subtitle_dic.keys()))
    print("匹配失败")
    return {}, []


# 媒体文件字幕匹配 关键字
def match_media_subtitle_auto(order_media_dic: dict, order_subtitle_dic: dict) -> dict:
    media_subtitle_dic = {}
    for order, media in order_media_dic.items():
        if order in order_subtitle_dic.keys():
            media_subtitle_dic[media] = order_subtitle_dic[order]
    return media_subtitle_dic


"""
由控制台直接调用
"""


# 翻译字幕
def translate_subtitles(subtitles_path: str, target_path: str, translate_dic: str = "./rule.csv",
                        reverse=False) -> int:
    result = 0
    init_translate_dic(translate_dic, reverse)
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


# 使用自动匹配移动原盘媒体文件
def move_bd_to_target(target_path, prefix, suffix, only_show, reverse, hardlink, *bd_path):
    # 搜索原盘目录
    dic_list = search_bd(*bd_path)
    if len(dic_list) == 0:
        print("找不到原盘文件")
        return 0
    if setting.debug:
        print(dic_list)
    media_list = match_bd_file_auto(*dic_list)
    order_media_dic = {order + 1: media_list[order] for order in range(len(media_list))}
    source_target_dic = {}
    for order, media_path in order_media_dic.items():
        new_filename = generate_filename(len(media_list), prefix, suffix, order) + "." + get_file_extension(media_path)
        source_target_dic[media_path] = os.path.join(target_path, new_filename)
    succeed, error = file_move(source_target_dic, only_show, hardlink=hardlink)
    return succeed if not only_show else len(source_target_dic)


# 移动bd文件到目录路径,指定数量
def move_bd_to_target_force_by_num(target_path: str, prefix: str, suffix: str, num: int, only_show: bool,
                                   reverse: bool, hardlink: bool, *BDMV_path: str) -> int:
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    if len(dic_list) == 0:
        print("找不到原盘文件")
        return 0
    # 计算数量
    avg_num = round(num / len(dic_list))
    media_list = match_bd_media_force_dynamic(num, avg_num, reverse, *dic_list)
    order_media_dic = {order + 1: media_list[order] for order in range(len(media_list))}
    source_target_dic = {}
    for order, media_path in order_media_dic.items():
        new_filename = generate_filename(num, prefix, suffix, order) + "." + get_file_extension(media_path)
        source_target_dic[media_path] = os.path.join(target_path, new_filename)
    succeed, error = file_move(source_target_dic, only_show, hardlink=hardlink)
    return succeed if not only_show else len(source_target_dic)


# 移动bd文件到目录路径,指定数量
def move_bd_to_target_force_by_each(target_path: str, prefix: str, suffix: str, num: int, each: int, only_show: bool,
                                    hardlink: bool, *BDMV_path: str) -> int:
    # 搜索原盘目录
    dic_list = search_bd(*BDMV_path)
    if num == 0:
        num = len(dic_list) * each
    media_list = match_bd_media_force_dynamic(num, each, False, *dic_list)
    order_media_dic = {order + 1: media_list[order] for order in range(len(media_list))}
    source_target_dic = {}
    for order, media_path in order_media_dic.items():
        new_filename = generate_filename(num, prefix, suffix, order) + "." + get_file_extension(
            media_path)
        source_target_dic[media_path] = os.path.join(target_path, new_filename)

    succeed, error = file_move(source_target_dic, only_show, hardlink=hardlink)
    return succeed if not only_show else len(source_target_dic)


# 原盘字幕匹配
def match_bd_subtitles(subtitle_path: str, target_path: str, prefix: str, suffix: str, each: int,
                       force: bool, only_show: bool, copy_subtitle: bool, reverse: bool, hardlink: bool,
                       *bd_path) -> int:
    subtitle_dic = scanning_subtitle(subtitle_path)
    if len(subtitle_dic) == 0:
        print("匹配字幕失败")
        return 0
    # 自动模式
    if not force:
        media_subtitle_dic, order_media_dic = match_bd_subtitle_auto(subtitle_dic, *bd_path)
    else:
        # 强制模式
        if each != 0:
            # 根据字幕数量和每个光盘文件中有效媒体的数量匹配
            media_subtitle_dic, order_media_dic = match_bd_subtitle_force_by_order_and_num(subtitle_dic, each, *bd_path)
        else:
            # 仅根据字幕数量强制匹配
            # 翻转代表为前多后少
            media_subtitle_dic, order_media_dic = match_bd_subtitle_force_by_subtitle(subtitle_dic, reverse, *bd_path)
    if len(media_subtitle_dic) == 0:
        print("匹配字幕和媒体文件失败")
        return 0
    if "" == target_path:
        return add_subtitle_for_media(media_subtitle_dic, only_show=only_show, copy_subtitle=copy_subtitle,
                                      hardlink=hardlink)
    else:
        return move_media_subtitle_to_new_path(media_subtitle_dic=media_subtitle_dic,
                                               order_media_dic=order_media_dic,
                                               target_dir=target_path, suffix=suffix, prefix=prefix,
                                               only_show=only_show, copy_subtitle=copy_subtitle, hardlink=hardlink)


# 匹配媒体文件和字幕
def match_media_subtitles(media_path: str, subtitle_path: str, target_path: str, prefix: str, suffix: str,
                          only_show: bool, hardlink: bool, copy_subtitle: bool) -> int:
    subtitle_dic = scanning_subtitle(subtitle_path)
    order_media_dic = scanning_media(media_path)
    if setting.debug:
        print("subtitle_dic :", subtitle_dic)
        print("order_media_dic :", order_media_dic)
    if len(order_media_dic) == 0 or len(subtitle_dic) == 0:
        print("匹配异常,共匹配到字幕{}个,共匹配到媒体文件{}个".format(len(subtitle_dic), len(order_media_dic)))
        return 0
    # 匹配
    media_subtitle_dic = match_media_subtitle_auto(order_media_dic, subtitle_dic)
    if len(media_subtitle_dic) == 0:
        print("匹配失败")
    if "" == target_path:
        return add_subtitle_for_media(media_subtitle_dic=media_subtitle_dic, only_show=only_show,
                                      copy_subtitle=copy_subtitle, hardlink=hardlink)
    else:
        return move_media_subtitle_to_new_path(media_subtitle_dic=media_subtitle_dic,
                                               order_media_dic=order_media_dic,
                                               target_dir=target_path, suffix=suffix, prefix=prefix,
                                               only_show=only_show, copy_subtitle=copy_subtitle, hardlink=hardlink)
