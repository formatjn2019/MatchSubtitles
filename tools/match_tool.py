import os
import re
import shutil

from utils.file_util import search_maxsize_file
from utils.match_util import replace_re_str, search_max_prefix_suffix

SUPPORT_SUBLIST = [
    "ass",
    "srt"
]

debug = True


# 根据名称和规则进行匹配
def match_by_rule(rule: re.Pattern, *names: str) -> (bool, dict):
    result = {}
    match_flag = True
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
    if len(namelist) < 4:
        print("文件数量过少")
        return {}
    # 根据前缀匹配
    prefix, suffix = search_max_prefix_suffix(*namelist)
    print("前后缀", prefix, "\t\t********\t\t", suffix)
    # 尝试对全部文件 完全匹配规则
    if len(prefix) > 0:
        rules = {
            # 采用前缀匹配的常规字符匹配
            "前缀规则": re.compile("^" + replace_re_str(prefix) + r"([0-9]{1,2}\.?5?|[0-9]|OVA|PV).*?$"),
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
                return order_dic
            else:
                print(rule_name, "匹配失败")
                print(namelist)
                for n in namelist:
                    print(n)

        # 完全匹配失败 尝试部分匹配
        most_prefix, most_suffix = search_max_prefix_suffix(*namelist, ratio=0.7)
        print("**--**" * 10)
        print(most_prefix, most_suffix)
        match_most_rule = re.compile(r"^{}.*{}$".format(replace_re_str(most_prefix), replace_re_str(most_suffix)))
        rules = {
            # 采用前缀匹配的常规字符匹配
            "前缀规则-部分": re.compile("^" + replace_re_str(most_prefix) + r"([0-9]{1,2}\.?5?|[0-9]|OVA|PV).*?$")
        }
        for rule_name, rule in rules.items():
            most_names = [name for name in namelist if match_most_rule.match(name)]
            print(len(most_names))
            match_succeed, order_dic = match_by_rule(rule, *most_names)
            # 成功匹配到对应的序号
            if match_succeed:
                print(rule_name, "匹配成功")
                print(order_dic)
                return order_dic
            else:
                print(rule_name, "匹配失败")
                print(namelist)
                for n in namelist:
                    print(n)

        print("全部尝试匹配失败")
    else:
        print("无法找到公共前缀")
    return {}


# 扫描字幕文件
def scanning_subtitle(subtitles_path: str) -> dict:
    print("路径", subtitles_path)
    suffix, current_count = "", 0
    # 后缀统计 二级后缀统计  名称统计
    suffix_count, language_suffix_count, name_count = {}, {}, {}
    for filename in os.listdir(subtitles_path):
        # print(filename)
        point_count = filename.count(".")
        if point_count > 0:
            # print(filename)
            # 后缀及其统计
            suffix_index = filename.rindex(".")
            temp_suffix = filename[suffix_index + 1:]
            suffix_count[temp_suffix] = suffix_count.get(temp_suffix, 0) + 1
            # 后缀处于支持格式中
            if temp_suffix in SUPPORT_SUBLIST:
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
    order_name_dic = parse_names(*name_count.keys())

    result = {}
    # 匹配成功后进行内容重组
    if not len(order_name_dic) == 0:
        for index, names in order_name_dic.items():
            print("{}\t{}\t{}".format("*" * 50, index, "*" * 50))
            if index not in result.keys():
                result[index] = []
            for name in names:
                for language_suffix in language_suffix_count.keys():
                    sp = os.path.join(subtitles_path,
                                      ".".join([item for item in [name, language_suffix, suffix] if len(item) > 0]))
                    print(sp)
                    if os.path.exists(sp):
                        result[index].append(sp)

    if debug:
        print("路径", subtitles_path)
        print("后缀:", suffix, "统计", current_count)
        print("后缀统计", suffix_count)
        print("二级后缀统计", language_suffix_count)
        print("名称统计", name_count)
        for k, v in result.items():
            print(k, v)
    return result


# 搜索原盘目录
def search_bd(*paths: str) -> dict:
    result = {}
    for path in paths:
        if not os.path.exists(path) or not os.path.isdir(path):
            return result
        sub_dir = os.listdir(path)
        if "BDMV" in sub_dir:
            metadir = os.listdir(os.path.join(path, "BDMV"))
            if "STREAM" in metadir and "PLAYLIST" in metadir:
                result[os.path.basename(path)] = path
        else:
            subs = search_bd(*[os.path.join(path, name) for name in os.listdir(path)])
            for k, v in subs.items():
                result[k] = v
    return result


# 匹配原盘文件
# 注 bd_paths 必须是按照光盘文件的顺序，不然会出错
def match_bd_metia(expect: int, *bd_paths: str) -> list:
    result = []
    # 能精准匹配
    if expect % len(bd_paths) == 0:
        # 预估剧集数量
        episodes_num = int(expect / len(bd_paths))
        for bd_path in bd_paths:
            print(bd_path)
            media_files = search_maxsize_file(episodes_num, os.path.join(bd_path, "BDMV", "STREAM"), suffix="m2ts")
            print(media_files)
            # 无法获取到期望数量的媒体文件
            if len(media_files) != episodes_num:
                return []
            else:
                for media_file_name in media_files:
                    result.append(os.path.join(bd_path, "BDMV", "STREAM", media_file_name))
    return result


# 匹配原盘文件
# 注 bd_paths 必须是按照光盘文件的顺序，不然会出错
def match_bd_metia_force(expect: int, per_number: int, *bd_paths: str) -> list:
    result = []
    # 强制顺序匹配
    for bd_path in bd_paths:
        print(bd_path)
        media_files = search_maxsize_file(per_number, os.path.join(bd_path, "BDMV", "STREAM"), suffix="m2ts")
        print(media_files)
        # 无法获取到期望数量的媒体文件
        if len(media_files) != per_number and len(result) < expect:
            return []
        else:
            for media_file_name in media_files:
                result.append(os.path.join(bd_path, "BDMV", "STREAM", media_file_name))
    return result[:expect]


# 为媒体文件添加字幕
# 注 多次运行会进行字幕的覆盖
def add_subtitle_for_metia(metia_subtitle_dic: dict, only_show: bool = True) -> int:
    replace_count = 0
    subtitle_set = set()
    for metia_path, subtitles in metia_subtitle_dic.items():
        print(metia_path)
        replace_count += 1
        metia_dir = os.path.dirname(metia_path)
        metia_name = os.path.basename(metia_path)
        metia_name = metia_name[:metia_name.index(".")]
        order = 0
        for subtitle_path in subtitles:
            subtitle_name = os.path.basename(subtitle_path)
            subtitle_suffix = subtitle_name[subtitle_name.find(".") + 1:]
            new_subtitle_path = os.path.join(metia_dir, ".".join([metia_name, subtitle_suffix]))
            while new_subtitle_path in subtitle_set:
                # 当字幕已存在时，重新生成字幕名
                new_subtitle_path = os.path.join(metia_dir, ".".join([metia_name, str(order), subtitle_suffix]))
                order += 1
            else:
                subtitle_set.add(new_subtitle_path)
            if only_show:
                print(subtitle_path, "----->", new_subtitle_path)
            else:
                print(subtitle_path, "已替换为-->", new_subtitle_path)
                shutil.copyfile(subtitle_path, new_subtitle_path)
    return replace_count
