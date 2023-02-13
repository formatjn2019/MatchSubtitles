import sys
import argparse

from rule.rules import translate_subtitles, move_bd_to_target_force_by_num, move_bd_to_target_force_by_each, \
    match_bd_subtitles
from setting import setting
from utils import check_rule

version = setting.version

parser = argparse.ArgumentParser(description="used for test")
media_group = parser.add_mutually_exclusive_group()

# 原盘文件路径
media_group.add_argument('--bdmv', '-b', action='append', dest='bd_path', help=('Blu-ray Disc file path'))
# 复制
parser.add_argument('--copy', '-c', action='store_true', dest='copy_subtitle', default=False, help=('copy'))
# 调试
parser.add_argument('--debug', '-d', action='store_true', help='debug', default=False)
# 每个光盘文件夹有效媒体的数量
parser.add_argument('--each', '-e', dest='each', type=int, help='Number of media files in each')
# 强制模式
parser.add_argument('--force', '-f', action='store_true', dest='force', help='Forced mode', default=False)
# 数量
parser.add_argument('--num', '-n', dest='number', type=int, help='number of media')
# 前缀
parser.add_argument('--prefix', '-pf', dest='prefix', help='File name prefix')
# 显示
parser.add_argument('--print', '-p', action='store_true', dest='only_print', help='Only print on the console',
                    default=False)
# 后缀
parser.add_argument('--suffix', '-sf', dest='suffix', help='File name suffix')
# 字幕文件夹
parser.add_argument('--subtitle', '-s', dest='subtitle', help='Path of subtitles')
# 翻译
parser.add_argument('--translate', '-tr', action='store_true', help='Translate subtitles', default=False)
# 目标路径
parser.add_argument('--target', '-t', dest='target_path', help='Target Path')
# 版本
parser.add_argument('--version', '-V', action='version', version='%(prog)s version : {}'.format(version),
                    help='Show the version')
# 详细
parser.add_argument('--verbosity', '-v', action='store_true', help='Increase output verbosity', default=False)
# 通用媒体文件路径
media_group.add_argument('--media', '-m', dest='media_path', help=('Media file path'))

# 放弃枚举，采用程序判定
allow_parameters = {
    "s.t": "翻译字幕",
    "c.s.t.tr": "翻译到目标目录",
    "b.s": "匹配字幕到原盘路径,移动字幕",
    "b.c.s": "匹配字幕到原盘路径,复制字幕",
    "b.p.s": "匹配字幕到原盘路径,仅显示",
    "b.c.p.s": "匹配字幕到原盘路径,仅显示",
    "b.s.t": "匹配字幕，媒体文件到目标路径,移动字幕",
    "b.c.s.t": "匹配字幕，媒体文件到目标路径,复制字幕",
    "b.p.s.t": "匹配字幕，媒体文件到目标路径,仅显示",
    "b.c.p.s.t": "匹配字幕，媒体文件到目标路径,仅显示",
    "b.f.s": "强制匹配字幕到原盘路径,移动",
    "b.c.f.s": "强制匹配字幕到原盘路径,复制",
    "b.f.p.s": "强制匹配字幕到原盘路径，仅显示",
    "b.c.f.p.s": "强制匹配字幕到原盘路径，仅显示",
    "b.f.s.t": "强制匹配字幕，媒体文件到目标路径,",
    "b.c.f.s.t": "强制匹配字幕，媒体文件到目标路径,复制",
    "b.f.p.s.t": "强制匹配字幕，媒体文件到目标路径,仅显示",
    "b.c.f.p.s.t": "强制匹配字幕，媒体文件到目标路径,仅显示",
    "b.e.f.s": "强制匹配字幕到原盘路径,并指定每个光盘文件夹中媒体文件的数量，移动",
    "b.c.e.f.s": "强制匹配字幕到原盘路径,并指定每个光盘文件夹中媒体文件的数量,复制",
    "b.e.f.p.s": "强制匹配字幕到原盘路径,并指定每个光盘文件夹中媒体文件的数量，仅显示",
    "b.c.e.f.p.s": "强制匹配字幕到原盘路径,并指定每个光盘文件夹中媒体文件的数量，仅显示",
    "b.e.f.s.t": "强制匹配字幕，媒体文件到目标路径,并指定每个光盘文件夹中媒体文件的数量,移动",
    "b.c.e.f.s.t": "强制匹配字幕，媒体文件到目标路径,并指定每个光盘文件夹中媒体文件的数量,复制",
    "b.e.f.p.s.t": "强制匹配字幕，媒体文件到目标路径,并指定每个光盘文件夹中媒体文件的数量，仅显示",
    "b.c.e.f.p.s.t": "强制匹配字幕，媒体文件到目标路径,并指定每个光盘文件夹中媒体文件的数量，仅显示",
    "m.s": "媒体文件和字幕匹配",
    "c.m.s": "媒体文件和字幕匹配,复制字幕",
    "m.p.s": "媒体文件和字幕匹配,仅打印",
    "c.m.p.s": "媒体文件和字幕匹配,仅打印",
    "m.s.t": "媒体文件和字幕匹配,指定目标路径",
    "c.m.s.t": "媒体文件和字幕匹配,指定目标路径,复制字幕",
    "m.p.s.t": "媒体文件和字幕匹配,仅打印,指定目标路径,仅打印",
    "c.m.p.s.t": "媒体文件和字幕匹配,仅打印,指定目标路径,仅打印",
}


# 生成可允许的队列
def generate_allows() -> dict:
    allowed = []
    # 原盘或媒体,字幕三种操作
    for opt in [["b", "s"], ["b", "f", "s"], ["b", "f", "s", "e"], ["m", "s"]]:
        tp = [opt]
        # 复制
        tp.extend([[*opt, "c"] for opt in tp if "s" in opt])
        # 添加目标路径
        tp.extend([[*opt, "t"] for opt in tp])
        allowed.extend(tp)
    for opt in [*allowed, ["b", "f", "n", "t"], ["b", "f", "e", "t"], ["b", "f", "e", "n", "t"]]:
        tp = [opt]
        # 前缀
        tp.extend([[*opt, "pf"] for opt in tp if "t" in opt])
        # 后缀
        tp.extend([[*opt, "sf"] for opt in tp if "t" in opt])
        # 打印
        tp.extend([[*opt, "p"] for opt in tp])
        allowed.extend(tp)

    # 特殊情况
    # 仅翻译字幕
    allowed.append(["tr", "s"])
    # 翻译字幕指定路径
    allowed.append(["tr", "s", "t"])
    # 详细信息
    allowed.extend([[*opt, "v"] for opt in allowed])
    # 调试
    allowed.extend([[*opt, "d"] for opt in allowed])
    return {translate_arr(*allow)[0]: translate_arr(*allow)[1] for allow in allowed if len(allow) > 1}


def translate_arr(*args: str) -> (str, str):
    explain = {
        "b": ("原盘", 1),
        "c": ("复制", 5),
        "d": ("debug", 16),
        "e": ("每个文件", 2),
        "f": ("强制", 0),
        "m": ("媒体", 1),
        "n": ("数量", 4),
        "p": ("仅显示", 14),
        "s": ("字幕", 6),
        "t": ("至目标", 11),
        "v": ("详细信息", 15),
        "tr": ("翻译", 4),
        "pf": ("指定前缀", 9),
        "sf": ("指定后缀", 10),
    }
    return ".".join(sorted(args)), " ".join([explain[key][0] for key in sorted(args, key=lambda x: explain[x][1])])


if __name__ == '__main__':

    # for k, v in generate_allows().items():
    #     # if k not in allow_parameters.keys():
    #         print(k, v)
    # exit(0)
    args = parser.parse_args()
    bd_path = args.bd_path
    target_path = args.target_path
    copy_subtitle = args.copy_subtitle
    subtitle = args.subtitle
    debug = args.debug
    each = args.each
    force = args.force
    media_path = args.media_path
    number = args.number
    prefix = args.prefix
    suffix = args.suffix
    translate = args.translate
    verbosity = args.verbosity
    only_print = args.only_print
    # 参数信息获取及有效性核验
    args_dic = {
        "b": (bd_path, *((True, "") if not bd_path else check_rule.check_path(*bd_path, isdir=True))),
        "s": (subtitle, *((True, "") if not subtitle else check_rule.check_path(subtitle, isdir=True))),
        "d": (debug, True, ""),
        "c": (copy_subtitle, True, ""),
        "e": (each, True, ""),
        "f": (force, True, ""),
        "m": (media_path, *((True, "") if not media_path else check_rule.check_path(*media_path, isdir=True))),
        "t": (target_path, *((True, "") if not target_path else check_rule.check_path(target_path, isdir=True))),
        "n": (number, True, ""),
        "pf": (prefix, True, ""),
        "p": (only_print, True, ""),
        "sf": (suffix, True, ""),
        "tr": (translate, True, ""),
        "v": (verbosity, True, ""),
    }
    # 放弃枚举，采用程序判定
    allow_parameters = generate_allows()
    arg_list = sorted([arg for arg in args_dic.keys() if args_dic[arg][0]])
    arg_str = ".".join([arg for arg in arg_list])
    select_arg_str = ".".join([arg for arg in arg_list if arg not in ["d", "v", "sf", "pf", "p", "c"]])
    print(select_arg_str)
    error_list = [k for k, v in args_dic.items() if not v[1]]
    print(args_dic)
    if len(error_list) > 0:
        print("error", error_list)
        exit(0)
    if verbosity:
        setting.verbosity = True
        print("详细信息开启")
    if debug:
        setting.debug = True
        setting.verbosity = True
        print("调试开启")
    # 翻译字幕
    # 翻译字幕指定文件夹
    if arg_str not in allow_parameters.keys():
        print("不允许的参数")
        print(arg_str)
        exit(1)
    # 翻译字幕
    if select_arg_str == "s.tr" or select_arg_str == "s.t.tr":
        print(setting.verbosity)
        translate_count = translate_subtitles(subtitles_path=subtitle, target_path=target_path)
        print("共翻译成功{}个".format(translate_count))
        pass
    elif select_arg_str == "b.f.n.t":
        print("数量匹配")
        # 提取目标bd文件到目标位置 指定数量
        move_bd_to_target_force_by_num(target_path=target_path, prefix=prefix, suffix=suffix, num=number,
                                       only_show=only_print, *bd_path)
    elif select_arg_str in ["b.e.f.t", "b.e.f.n.t"]:
        print("数量,每个匹配")
        # 提取目标bd文件到目标位置 指定每个，可选总数
        move_bd_to_target_force_by_each(target_path=target_path, prefix=prefix, suffix=suffix, num=number, each=each,
                                        only_show=only_print,
                                        *bd_path)
    elif select_arg_str in [["b", "s"], ["b", "f", "s"], ["b", "f", "s", "e"]]:
        print("匹配原盘")

        match_bd_subtitles(subtitle_path=subtitle, target_path=target_path, prefix=prefix, suffix=suffix, each=each,
                           num=number, force=force, copy_subtitle=copy_subtitle, only_show=only_print)

    pass
elif arg_str == "s.t":
    pass
elif arg_str == "s.t":
    pass
elif arg_str == "s.t":
    pass

if bd_path:
    print("原盘路径开启")
if subtitle:
    print("字幕开启")

if each:
    print("每个文件开启")
if force:
    print("强制模式开启")
if media_path:
    print("媒体开启")
if number:
    print("数量开启")
if prefix:
    print("前缀开启")
if suffix:
    print("后缀开启")
if translate:
    print("翻译开启")

if target_path:
    print("目标路径开启")
if only_print:
    print("仅打印开启")
if copy_subtitle:
    print("复制开启")
# print(args)
# print(sys.argv)
# print(sys.orig_argv)
