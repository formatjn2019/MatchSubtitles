import os
import re

from utils.file_util import search_maxsize_file
from utils.match_util import replace_re_str, search_max_prefix_suffix
from setting import setting


# 根据名称和规则进行匹配
def match_by_rule(rule: re.Pattern, *names: str) -> (bool, dict):
    result, match_flag = {}, True
    for n in names:
        match = rule.match(n)
        match_flag = match_flag and bool(match)
        # 匹配成功
        if match_flag:
            if not result.get(match.group(1)):
                result[match.group(1)] = []
            result[match.group(1)].append(n)
    # 成功匹配到对应的序号
    return match_flag and sum(len(item) for item in result.values()) == len(names), result


# 解析名称
def parse_names(*namelist: str) -> dict:
    # 文件过少不会进行匹配
    if len(namelist) < 4:
        print("文件数量过少")
        return {}
    # 根据前缀匹配
    prefix, suffix = search_max_prefix_suffix(*namelist)
    if setting.verbosity:
        print("前后缀", prefix, "\t\t《********》\t\t", suffix)
    # 尝试对全部文件 完全匹配规则
    if len(prefix) > 0:
        rules = {
            # 采用前缀匹配的常规字符匹配
            "前缀规则": re.compile("^" + replace_re_str(prefix) + r"([0-9]{1,4}\.?5?|[0-9]|OVA|PV).*?$"),
            # 带有括号的前后缀统一匹配规则
            "前后缀规则-括号": re.compile(r"^{}\[(\w+)]{}$".format(replace_re_str(prefix), replace_re_str(suffix))),
            # 前后缀统一的单词匹配
            "前后缀规则-单词": re.compile(r"^{} ?([\w ]+) ?{}$".format(replace_re_str(prefix), replace_re_str(suffix))),
            # 仅根据固定前缀进行匹配，忽略尾部[]内容
            "前缀规则-括号": re.compile(r"^{}\[?(\w+)](\[.*?] ?)*$".format(replace_re_str(prefix))),
        }
        for rule_name, rule in rules.items():
            match_succeed, order_dic = match_by_rule(rule, *namelist)
            # 成功匹配到对应的序号
            if match_succeed:
                print(rule_name, "匹配成功")
                if setting.debug:
                    print(order_dic)
                return order_dic
            else:
                print(rule_name, "匹配失败")
                if setting.debug:
                    print(namelist)

        # 完全匹配失败 尝试部分匹配 比例为0.7
        most_prefix, most_suffix = search_max_prefix_suffix(*namelist, ratio=0.7)
        if setting.verbosity:
            print("**--**" * 10)
            print(most_prefix, most_suffix)
        match_most_rule = re.compile(r"^{}.*{}$".format(replace_re_str(most_prefix), replace_re_str(most_suffix)))
        rules = {
            # 采用前缀匹配的常规字符匹配
            "前缀规则-部分": re.compile("^" + replace_re_str(most_prefix) + r"([0-9]{1,4}\.?5?|[0-9]|OVA|PV).*?$")
        }
        for rule_name, rule in rules.items():
            most_names = [name for name in namelist if match_most_rule.match(name)]
            match_succeed, order_dic = match_by_rule(rule, *most_names)
            # 成功匹配到对应的序号
            if match_succeed:
                print(rule_name, "匹配成功")
                if setting.debug:
                    print(order_dic)
                return order_dic
            else:
                print(rule_name, "匹配失败")
                if setting.debug:
                    print(namelist)
        print("全部尝试匹配失败")
    else:
        print("无法找到公共前缀")
    return {}


def scanning_media(media_path: str) -> dict:
    if setting.verbosity:
        print("路径", media_path)
    name_count, suffix_count = {}, {}
    suffix, current_count = "", 0
    for filename in os.listdir(media_path):
        if filename.count(".") > 0:
            # 后缀及其统计
            temp_suffix = filename[filename.rindex(".") + 1:]
            # 后缀处于支持格式中
            if temp_suffix in setting.SUPPORT_MEDIA_LIST:
                # 更新后缀最大值统计
                if suffix_count.get(temp_suffix, 1) > current_count:
                    suffix, current_count = temp_suffix, suffix_count.get(temp_suffix, 1)
                suffix_count[temp_suffix] = suffix_count.get(temp_suffix, 0) + 1
                # 无后缀名称
                file_name = filename[:-len(temp_suffix) - 1]
                name_count[file_name] = name_count.get(file_name, 0) + 1
    # 格式数量匹配
    if len(suffix_count) > 0:
        order_names_dic = parse_names(*name_count.keys())
        order_name_dic = {order: os.path.join(media_path, names[0] + "." + suffix) for order, names in
                          order_names_dic.items()}
        if len(order_name_dic) != sum(len(names) for _, names in order_names_dic.items()):
            print("警告 媒体匹配不完全")
    else:
        print("媒体格式多于一种，无法匹配")
        return {}
    if setting.debug:
        print("name_count: ", name_count)
        print("suffix_count: ", suffix_count)
        print("匹配到", len(order_name_dic), "个")
    return order_name_dic


# 扫描字幕文件
def scanning_subtitle(subtitles_path: str) -> dict:
    if setting.verbosity:
        print("路径", subtitles_path)
    suffix, current_count = "", 0
    # 后缀统计 二级后缀统计  名称统计
    suffix_count, language_suffix_count, name_count = {}, {}, {}
    for filename in os.listdir(subtitles_path):
        point_count = filename.count(".")
        if point_count > 0:
            # 后缀及其统计
            suffix_index = filename.rindex(".")
            temp_suffix = filename[suffix_index + 1:]
            suffix_count[temp_suffix] = suffix_count.get(temp_suffix, 0) + 1
            # 后缀处于支持格式中
            if temp_suffix in setting.SUPPORT_SUBLIST:
                # 更新后缀最大值统计
                if suffix_count[temp_suffix] > current_count:
                    suffix, current_count = temp_suffix, suffix_count[temp_suffix]
                # 二级后缀及其统计
                if point_count > 1:
                    lsfx = filename[filename.rindex(".", 0, suffix_index) + 1:suffix_index]
                    language_suffix_count[lsfx] = language_suffix_count.get(lsfx, 0) + 1
                else:
                    language_suffix_count[""] = language_suffix_count.get("", 0) + 1
                # 名称截取
                # 有二级后缀，则截取二级，如无，则截取一级
                if point_count == 1:
                    file_name = filename[:filename.rfind(".")]
                else:
                    file_name = filename[:filename.rfind(".", 1, filename.rfind("."))]
                name_count[file_name] = name_count.get(file_name, 0) + 1

    # 找不到后缀
    if "" == suffix:
        print("错误！ 请输入正确字幕路径")
        return {}
    elif not (max(len(language_suffix_count), 1) * len(name_count) == suffix_count[suffix]):
        print("警告！ 字幕数量并非对其齐\n\n\n")
        print("*" * 100)
        for filename in os.listdir(subtitles_path):
            print(filename)
        print("*" * 100)
    # 但在未对其的情况下仍然尝试进行匹配
    order_names_dic = parse_names(*name_count.keys())

    result = {}
    # 匹配成功后进行内容重组
    if not len(order_names_dic) == 0:
        for index, names in order_names_dic.items():
            if setting.verbosity:
                print("{}\t{}\t{}".format("*" * 50, index, "*" * 50))
            if index not in result.keys():
                result[index] = []
            for name in names:
                for language_suffix in language_suffix_count.keys():
                    sp = os.path.join(subtitles_path,
                                      ".".join([item for item in [name, language_suffix, suffix] if len(item) > 0]))
                    if setting.verbosity:
                        print(sp)
                    if os.path.exists(sp):
                        result[index].append(sp)

    if setting.debug:
        print("路径", subtitles_path)
        print("后缀:", suffix, "统计", current_count)
        print("后缀统计", suffix_count)
        print("二级后缀统计", language_suffix_count)
        print("名称统计", name_count)
        for k, v in result.items():
            print(k, v)
    return result


# 搜索原盘目录
# 根据文件夹名或路径进行排序
def _search_bd(*paths: str) -> list:
    result = []
    for path in paths:
        if not os.path.exists(path) or not os.path.isdir(path):
            return result
        sub_dir = os.listdir(path)
        if "BDMV" in sub_dir:
            metadir = os.listdir(os.path.join(path, "BDMV"))
            if "STREAM" in metadir and "PLAYLIST" in metadir:
                result.append((os.path.basename(path), path))
        else:
            for sub in _search_bd(*[os.path.join(path, name) for name in os.listdir(path) if
                                    os.path.isdir(os.path.join(path, name))]):
                result.append(sub)
    return result


# 搜索原盘目录
# 根据文件夹名或路径进行排序
def search_bd(*paths: str) -> list:
    # 根据文件夹名或路径排序
    # 不同路径 根据路径排序，同一路径，根据文件名排序
    return [path for _, path in sorted(_search_bd(*paths), key=lambda key: (key[0], key[1]))]


# 匹配原盘文件
# 根据期望数量匹配
# 注 bd_paths 必须是按照光盘文件的顺序，不然会出错
def match_bd_media(expect: int, *bd_paths: str) -> list:
    result = []
    # 能精准匹配
    if expect % len(bd_paths) == 0:
        # 预估剧集数量
        episodes_num = int(expect / len(bd_paths))
        for bd_path in bd_paths:
            media_files = search_maxsize_file(episodes_num, os.path.join(bd_path, "BDMV", "STREAM"), suffix="m2ts")
            if setting.verbosity:
                print(bd_path, media_files)
            # 无法获取到期望数量的媒体文件
            if len(media_files) != episodes_num:
                return []
            else:
                for media_file_name in media_files:
                    result.append(os.path.join(bd_path, "BDMV", "STREAM", media_file_name))
    return result


# 匹配原盘文件
# 指定每个光盘数量剧集，强制匹配
# 注 bd_paths 必须是按照光盘文件的顺序，不然会出错
def match_bd_media_force_each(expect: int, each: int, *bd_paths: str) -> list:
    result = []
    # 强制顺序匹配
    for bd_path in bd_paths:
        media_files = search_maxsize_file(each, os.path.join(bd_path, "BDMV", "STREAM"), suffix="m2ts")
        if setting.verbosity:
            print(bd_path, media_files)
        # 无法获取到期望数量的媒体文件
        if len(media_files) != each and len(result) < expect:
            return []
        else:
            for media_file_name in media_files:
                result.append(os.path.join(bd_path, "BDMV", "STREAM", media_file_name))
    return result[:expect]


# 匹配原盘文件
# 强制动态匹配
# 注 bd_paths 必须是按照光盘文件的顺序，不然会出错
def match_bd_media_force_dynamic(expect: int, per_number: int, *bd_paths: str) -> list:
    result, messages, remain = [], [], expect
    # 强制动态匹配
    for bd_path in bd_paths:
        if remain <= 0:
            break
        media_files = search_maxsize_file(per_number, os.path.join(bd_path, "BDMV", "STREAM"), suffix="m2ts")
        messages.append((bd_path, media_files))
        # 无法获取到期望数量的媒体文件
        if len(media_files) != per_number and len(result) < expect:
            return []
        else:
            for media_file_name in media_files:
                result.append(os.path.join(bd_path, "BDMV", "STREAM", media_file_name))
            remain -= per_number
    # 依旧有剩余未能全部匹配的
    if remain > 0:
        remain += per_number
        # 重新处理最后一个盘的文件
        result, messages = result[:-per_number], messages[:-1]
        media_files = search_maxsize_file(remain, os.path.join(bd_paths[-1], "BDMV", "STREAM"), suffix="m2ts")
        if len(media_files) < remain:
            print("自动匹配失败")
            return []
        for media_file_name in media_files:
            result.append(os.path.join(bd_paths[-1], "BDMV", "STREAM", media_file_name))
        messages.append((bd_paths[-1], media_files))

    if setting.debug:
        for message in messages:
            print(message[0], message[1])
    return result[:expect]
