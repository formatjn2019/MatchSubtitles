import re

from tools.match_tool import scanning_subtitle, search_bd, match_bd_metia, match_bd_metia_force

KEY_WORDS_RULE_DIC = {
    "全部匹配": re.compile(r"^.*$"),
    "数字及OVA,PV": re.compile(r"^\d+|OVA|PV$"),
    "数字及.5": re.compile(r"^\d+(\.5)?$"),
    "纯数字": re.compile(r"^\d+$"),
}

visual = True

# 根据路径匹配出标题字典和原盘路径序列
def search_bdmv_and_subtitles(BDMV_path, subtitles_dir) -> (dict, list):
    # 搜索字幕目录
    subtitle_dic = scanning_subtitle(subtitles_dir)
    print("共扫扫描到{}集字幕文件".format(len(subtitle_dic)))
    # 搜索原盘目录
    bddic = search_bd(BDMV_path)
    print("共扫扫描到{}个光盘文件".format(len(bddic)))
    dic_list = []
    # 将光盘排序后依次添加
    for k in sorted(bddic.keys()):
        print(k, bddic[k])
        dic_list.append(bddic[k])
    return subtitle_dic, dic_list

# 原盘剧集匹配
# 根据字幕动态匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_auto(BDMV_path: str, subtitles_dir: str) -> dict:
    subtitle_dic, dic_list = search_bdmv_and_subtitles(BDMV_path, subtitles_dir)
    for name, rule in KEY_WORDS_RULE_DIC.items():
        keywords = sorted([keyword for keyword in subtitle_dic.keys() if rule.match(keyword)])
        print("采用 {} 规则解析字幕 共{}集\n分别为\t{}".format(name, len(keywords), "\t".join(keywords)))
        # 尝试根据字幕数量完全匹配
        media_list = match_bd_metia(len(keywords), *dic_list)
        if len(media_list) > 0:
            result = {}
            for index in range(len(media_list)):
                result[media_list[index]] = subtitle_dic[keywords[index]]

            if visual:
                for index in range(len(media_list)):
                    print("剧集：\t{}\n媒体：\t{}".format(keywords[index], media_list[index]))
                    print("字幕：\t{}\n".format("\n\t\t".join(subtitle_dic[keywords[index]])))
            return result
    print("匹配失败")
    return {}


# 原盘剧集匹配
# 指定参数进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_subtitle_force_by_order(BDMV_path: str, subtitles_dir: str, per_number: int) -> dict:
    subtitle_dic, dic_list = search_bdmv_and_subtitles(BDMV_path, subtitles_dir)
    # 尝试根据字幕数量强制匹配
    media_list = match_bd_metia_force(len(subtitle_dic),per_number, *dic_list)
    if len(media_list) > 0:
        result = {}
        keywords= sorted(subtitle_dic.keys())
        for index in range(len(media_list)):
            result[media_list[index]] = subtitle_dic[keywords[index]]

        if visual:
            for index in range(len(media_list)):
                print("剧集：\t{}\n媒体：\t{}".format(keywords[index], media_list[index]))
                print("字幕：\t{}\n".format("\n\t\t".join(subtitle_dic[keywords[index]])))
        return result

