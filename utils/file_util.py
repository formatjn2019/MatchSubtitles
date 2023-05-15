import math
import os

from setting import setting


# 找到最大的n个文件
# file_path 为文件所在文件夹
# 根据指定后缀过滤
def search_maxsize_file(expect: int, file_root_path: str, suffix: str = "", *exclude: str) -> list:
    file_size_dic = {}
    for name in os.listdir(file_root_path):
        if not name.endswith(suffix):
            continue
        size = get_file_size(os.path.join(file_root_path, name))
        file_size_dic[name] = size
    result = list(file_size_dic.keys())
    # 排序后截取
    result.sort(key=file_size_dic.get, reverse=True)
    return sorted(result[:expect])


# 获取文件大小，当测试时，使用文件内容代替文件大小
def get_file_size(file_path: str) -> int:
    size = os.stat(file_path).st_size
    if setting.virtual_file:
        # 测试文件采用虚拟数值
        with open(file_path, "r", encoding="utf8") as f:
            size = int(f.read())
    return size


# 获取文件后缀
def get_file_extension(file_path: str) -> str:
    filename = os.path.basename(file_path)
    # .开头的隐藏忽略和没有后缀的忽略
    return filename[filename.find(".") + 1:] if filename.find(".") > 0 else ""


# 获取文件名
def get_file_name(file_path: str) -> str:
    filename = os.path.basename(file_path)
    return filename[:filename.find(".")] if filename.find(".") > 0 else filename


# 自动生成文件名
def generate_filename(size: int, prefix: str, suffix: str, order: any) -> str:
    prefix = prefix if prefix is not None else ""
    suffix = suffix if suffix is not None else ""
    # 数字格式化输出
    if type(order) == int:
        return "{}{:0>{}d}{}".format(prefix, order, math.ceil(math.log10(size + 1)), suffix)
    return "{}{}{}".format(prefix, order, suffix)
