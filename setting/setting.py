debug = False
verbosity = False
version = "v 0.1.1"
# 虚拟文件，文件内容为文本，文件的实际大小
# 仅单元测试使用，其它情况下无法打开
virtual_file = False


# 可选值
# avg_num size_rate variance_rate
# 3 1.7~2.3 6~7
# 4 1.6~2.4 6~7
# 文件大小平均值选取数量
AVG_NUM = 2
# 模拟得到到的极限值
# 文件大小比率
SIZE_RATE = 2.1
# 方差比率
VARIANCE_RATE = 7

SUPPORT_SUBLIST = [
    "ass",
    "srt",
    "ssa",
]

SUPPORT_MEDIA_LIST = [
    "avi",
    "flv",
    "m2ts",
    "mp4",
    "mkv",
    "ts",
    "wmv",
]
