import re

from tools.match_tool import scanning_subtitle, search_bd, match_bd_media, match_bd_media_force, \
    match_bd_media_force_dynamic

KEY_WORDS_RULE_DIC = {
    "全部匹配": re.compile(r"^.*$"),
    "数字及OVA,PV": re.compile(r"^\d+|OVA|PV$"),
    "数字及.5": re.compile(r"^\d+(\.5)?$"),
    "纯数字": re.compile(r"^\d+$"),
}

visual = True


def scanning_bdmv_path(BDMV_path: str) -> list:
    # 搜索原盘目录
    bd_dic = search_bd(BDMV_path)
    if visual:
        print("共扫描到{}个光盘文件".format(len(bd_dic)))
    dic_list = []
    # 将光盘排序后依次添加
    for k in sorted(bd_dic.keys()):
        print(k, bd_dic[k])
        dic_list.append(bd_dic[k])
    return dic_list


# 公共方法
# 字幕与媒体配对
def _match_media_subtitle(subtitle_dic: dict, media_list: list, *keywords) -> dict:
    result = {}
    for index in range(len(media_list)):
        result[media_list[index]] = subtitle_dic[keywords[index]]

    if visual:
        for index in range(len(media_list)):
            print("剧集：\t{}\n媒体：\t{}".format(keywords[index], media_list[index]))
            print("字幕：\t{}\n".format("\n\t\t".join(subtitle_dic[keywords[index]])))
    return result


# 原盘剧集匹配
# 根据字幕动态匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_auto(BDMV_path: str,  subtitle_dic: dict) -> dict:
    # # 搜索字幕目录
    # subtitle_dic = scanning_subtitle(subtitles_dir)
    # 搜索原盘目录
    dic_list = scanning_bdmv_path(BDMV_path)
    # subtitle_dic, dic_list = search_bdmv_and_subtitles(BDMV_path, subtitles_dir)
    # dic_list = search_bdmv_and_subtitles(BDMV_path, subtitles_dir)
    for name, rule in KEY_WORDS_RULE_DIC.items():
        keywords = sorted([keyword for keyword in subtitle_dic.keys() if rule.match(keyword)])
        print("采用 {} 规则解析字幕 共{}集\n分别为\t{}".format(name, len(keywords), "\t".join(keywords)))
        # 尝试根据字幕数量完全匹配
        media_list = match_bd_media(len(keywords), *dic_list)
        if len(media_list) > 0:
            return _match_media_subtitle(subtitle_dic, media_list, *keywords)
    print("匹配失败")
    return {}


# 原盘剧集匹配
# 指定每盘数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_order_and_num(BDMV_path: str, subtitle_dic: dict, per_number: int) -> dict:
    # # 搜索字幕目录
    # subtitle_dic = scanning_subtitle(subtitles_dir)
    # 搜索原盘目录
    dic_list = scanning_bdmv_path(BDMV_path)
    # 尝试根据字幕数量强制匹配
    media_list = match_bd_media_force(len(subtitle_dic), per_number, *dic_list)
    if len(media_list) > 0:
        return _match_media_subtitle(subtitle_dic, media_list, *sorted(subtitle_dic.keys()))
    print("匹配失败")
    return {}


# 原盘剧集匹配
# 指定每盘数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_subtitle(BDMV_path: str,  subtitle_dic: dict) -> dict:

    # 搜索原盘目录
    dic_list = scanning_bdmv_path(BDMV_path)
    # 计算数量
    avg_num = round(len(subtitle_dic) / len(dic_list))
    media_list = match_bd_media_force_dynamic(len(subtitle_dic), avg_num, *dic_list)
    if len(media_list) > 0:
        return _match_media_subtitle(subtitle_dic, media_list, *sorted(subtitle_dic.keys()))
    print("匹配失败")
    return {}
