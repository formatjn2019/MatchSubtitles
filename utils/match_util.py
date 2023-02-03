import re

RE_REPL_RULE = re.compile(r"([.*+?^$\[\]()\\])")


# 正则转义
def replace_re_str(origin_string: str) -> str:
    return RE_REPL_RULE.sub(r"\\\1", origin_string)


# 统计字符串 索引最多字母
def count_most_char_by_index(index: int, *names: str) -> str:
    result, mx = names[0][0], 0
    count_dic = {}
    for name in names:
        if index >= len(name):
            return result
        count_dic[name[index]] = count_dic.get(name[index], 0) + 1
        if count_dic[name[index]] > mx:
            result, mx = name[index], count_dic[name[index]]
    return result


# 寻找最大前缀后缀
def search_max_prefix_suffix(*namelist: str, ratio: float = 1):
    prefix, suffix, tp, ts = "", "", "", ""
    # 卫语句
    if len(namelist) == 0:
        return prefix, suffix
    # 搜索前缀
    while len(prefix) < len(namelist[0]):
        count = 0
        # 全匹配模式，按照第一个字符串，否则按照最高概率字符计算
        if ratio == 1:
            tp = namelist[0][:len(prefix) + 1]
        else:
            tp += count_most_char_by_index(len(prefix), *namelist)

        for n in namelist:
            if n.startswith(tp):
                count += 1
        # 根据统计比例判断是否继续
        if count / len(namelist) >= ratio:
            prefix = tp
            continue
        break
    # 搜索后缀
    while len(suffix) < len(namelist[0]) - len(prefix):
        count = 0
        if ratio == 1:
            ts = namelist[0][len(namelist[0]) - len(suffix) - 1:]
        else:
            ts = count_most_char_by_index(-1 * (len(suffix) + 1), *namelist) + ts
        for n in namelist:
            if n.endswith(ts):
                count += 1
        if count > 0 and count / len(namelist) >= ratio:
            suffix = ts
            continue
        break
    return prefix, suffix
