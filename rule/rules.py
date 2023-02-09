import re

from tools.match_tool import scanning_captions, search_bd, match_bd_media, match_bd_media_force, \
    match_bd_media_force_dynamic

KEY_WORDS_RULE_DIC = {
    "全部匹配": re.compile(r"^.*$"),
    "数字及OVA,PV": re.compile(r"^\d+|OVA|PV$"),
    "数字及.5": re.compile(r"^\d+(\.5)?$"),
    "纯数字": re.compile(r"^\d+$"),
}

visual = True



# 公共方法
# 字幕与媒体配对
def _match_media_caption(caption_dic: dict, media_list: list, *keywords) -> dict:
    result = {}
    for index in range(len(media_list)):
        result[media_list[index]] = caption_dic[keywords[index]]

    if visual:
        for index in range(len(media_list)):
            print("剧集：\t{}\n媒体：\t{}".format(keywords[index], media_list[index]))
            print("字幕：\t{}\n".format("\n\t\t".join(caption_dic[keywords[index]])))
    return result


# 原盘剧集匹配
# 根据字幕动态匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_caption_auto(BDMV_path: str, caption_dic: dict) -> (dict, list):
    # # 搜索字幕目录
    # caption_dic = scanning_caption(captions_dir)
    # 搜索原盘目录
    dic_list = search_bd(BDMV_path)
    # caption_dic, dic_list = search_bdmv_and_captions(BDMV_path, captions_dir)
    # dic_list = search_bdmv_and_captions(BDMV_path, captions_dir)
    for name, rule in KEY_WORDS_RULE_DIC.items():
        keywords = sorted([keyword for keyword in caption_dic.keys() if rule.match(keyword)])
        print("采用 {} 规则解析字幕 共{}集\n分别为\t{}".format(name, len(keywords), "\t".join(keywords)))
        # 尝试根据字幕数量完全匹配
        media_list = match_bd_media(len(keywords), *dic_list)
        if len(media_list) > 0:
            return _match_media_caption(caption_dic, media_list, *keywords), media_list
    print("匹配失败")
    return {}, []


# 原盘剧集匹配
# 指定每盘数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_caption_force_by_order_and_num(BDMV_path: str, caption_dic: dict, per_number: int) -> (dict, list):
    # # 搜索字幕目录
    # caption_dic = scanning_caption(captions_dir)
    # 搜索原盘目录
    dic_list = search_bd(BDMV_path)
    # 尝试根据字幕数量强制匹配
    media_list = match_bd_media_force(len(caption_dic), per_number, *dic_list)
    if len(media_list) > 0:
        return _match_media_caption(caption_dic, media_list, *sorted(caption_dic.keys())), media_list
    print("匹配失败")
    return {}, []


# 原盘剧集匹配
# 指定每盘数量 进行强制数量匹配
# 字典格式 媒体路径:[字幕路径]
def match_bd_caption_force_by_caption(BDMV_path: str, caption_dic: dict) -> (dict, list):
    # 搜索原盘目录
    dic_list = search_bd(BDMV_path)
    # 计算数量
    avg_num = round(len(caption_dic) / len(dic_list))
    media_list = match_bd_media_force_dynamic(len(caption_dic), avg_num, *dic_list)
    if len(media_list) > 0:
        return _match_media_caption(caption_dic, media_list, *sorted(caption_dic.keys())), media_list
    print("匹配失败")
    return {}, []


# 媒体文件字幕匹配 关键字
def match_media_caption_auto(order_media_dic: dict, order_caption_dic: dict) -> (dict, list):
    media_caption_dic, orders = {}, []
    for order, media in order_media_dic.items():
        if order in order_caption_dic.keys():
            media_caption_dic[media] = order_caption_dic[order]
    return media_caption_dic, [order_media_dic[order] for order in sorted(orders)]
