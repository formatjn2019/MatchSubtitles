import os

debug = False


# 找到最大的n个文件
# file_path 为文件所在文件夹
# 根据指定后缀过滤
def search_maxsize_file(expect: int, file_root_path: str, suffix: str = "", *exclude: str) -> list:
    file_size_dic = {}
    for name in os.listdir(file_root_path):
        if not name.endswith(suffix):
            continue
        file_path = os.path.join(file_root_path, name)
        size = os.stat(file_path).st_size
        if debug:
            # 测试文件采用虚拟数值
            with open(file_path, "r", encoding="utf8") as f:
                size = int(f.read())
        file_size_dic[name] = size
    result = list(file_size_dic.keys())
    # 排序后截取
    result.sort(key=file_size_dic.get, reverse=True)
    return sorted(result[:expect])
