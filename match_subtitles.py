import sys
import argparse

from rule.rules import translate_subtitles, move_bd_to_target, move_bd_to_target_force_by_num, \
    move_bd_to_target_force_by_each, \
    match_bd_subtitles, match_media_subtitles
from setting import setting
from utils import check_rule

version = setting.version

parser = argparse.ArgumentParser(description="used for test")
media_group = parser.add_mutually_exclusive_group()

# 原盘文件路径
media_group.add_argument('--bdmv', '-b', action='append', dest='bd_path', help='Blu-ray Disc file path')
# 复制
parser.add_argument('--copy', '-c', action='store_true', dest='copy_subtitle', default=False, help='copy')
# 调试
parser.add_argument('--debug', '-d', action='store_true', help='debug', default=False)
# 每个光盘文件夹有效媒体的数量
parser.add_argument('--each', '-e', dest='each', type=int, help='Number of media files in each')
# 强制模式
parser.add_argument('--force', '-f', action='store_true', dest='force', help='Forced mode', default=False)
# 显示
parser.add_argument('--hardlink', '-l', action='store_true', dest='hardlink', help='hardlink files', default=False)
# 通用媒体文件路径
media_group.add_argument('--media', '-m', dest='media_path', help='Media file path')
# 数量
parser.add_argument('--num', '-n', dest='number', type=int, help='number of media')
# 前缀
parser.add_argument('--prefix', '-pf', dest='prefix', help='File name prefix')
# 显示
parser.add_argument('--print', '-p', action='store_true', dest='only_print', help='Only print on the console',
                    default=False)
# 翻转
parser.add_argument('--reverse', '-r', action='store_true', dest='reverse', help='reverse', default=False)
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


# 生成可允许的队列
def generate_allows() -> dict:
    allowed = []
    # 原盘或媒体,字幕三种操作
    for opt in [["b", "s"], ["b", "f", "s"], ["b", "f", "r", "s"], ["b", "f", "s", "e"], ["m", "s"]]:
        tp = [opt]
        # 复制
        tp.extend([[*opt, "c"] for opt in tp if "s" in opt])
        # 添加目标路径
        tp.extend([[*opt, "t"] for opt in tp])
        allowed.extend(tp)
    for opt in [*allowed, ["b", "t"], ["b", "f", "n", "t"], ["b", "f", "n", "r", "t"], ["b", "f", "e", "t"],
                ["b", "f", "e", "n", "t"]]:
        tp = [opt]
        # 前缀
        tp.extend([[*opt, "pf"] for opt in tp if "t" in opt])
        # 后缀
        tp.extend([[*opt, "sf"] for opt in tp if "t" in opt])
        # 打印
        tp.extend([[*opt, "p"] for opt in tp])
        # 硬链接
        tp.extend([[*opt, "l"] for opt in tp])
        allowed.extend(tp)

    # 特殊情况
    # 仅翻译字幕
    allowed.append(["tr", "s"])
    allowed.append(["tr", "r", "s"])
    # 翻译字幕指定路径
    allowed.append(["tr", "s", "t"])
    allowed.append(["tr", "r", "s", "t"])
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
        "l": ("硬链接", 11),
        "m": ("媒体", 1),
        "n": ("数量", 4),
        "p": ("仅显示", 14),
        "s": ("字幕", 6),
        "t": ("至目标", 12),
        "v": ("详细信息", 15),
        "tr": ("翻译", 4),
        "pf": ("指定前缀", 9),
        "r": ("翻转", 13),
        "sf": ("指定后缀", 10),
    }
    return ".".join(sorted(args)), " ".join([explain[key][0] for key in sorted(args, key=lambda x: explain[x][1])])


if __name__ == '__main__':
    args = parser.parse_args()
    bd_path = args.bd_path
    copy_subtitle = args.copy_subtitle
    subtitle = args.subtitle
    setting.debug = debug = args.debug
    each = args.each if args.each is not None else 0
    force = args.force
    hardlink = args.hardlink
    media_path = args.media_path
    number = args.number if args.number is not None else 0
    prefix = args.prefix if args.prefix is not None else ""
    reverse = args.reverse
    suffix = args.suffix if args.suffix is not None else ""
    target_path = args.target_path if args.target_path is not None else ""
    translate = args.translate
    setting.verbosity = verbosity = args.verbosity or args.debug
    only_print = args.only_print

    # 参数信息获取及有效性核验
    args_dic = {
        "b": (bd_path, *((True, "") if not bd_path else check_rule.check_path(*bd_path, isdir=True))),
        "s": (subtitle, *((True, "") if not subtitle else check_rule.check_path(subtitle, isdir=True))),
        "d": (debug, True, ""),
        "c": (copy_subtitle, True, ""),
        "e": (each, True, ""),
        "f": (force, True, ""),
        "l": (hardlink, True, ""),
        "m": (media_path, *((True, "") if not media_path else check_rule.check_path(media_path, isdir=True))),
        "t": (target_path, *((True, "") if not target_path else check_rule.check_path(target_path, isdir=True))),
        "n": (number, True, ""),
        "pf": (prefix, True, ""),
        "p": (only_print, True, ""),
        "r": (reverse, True, ""),
        "sf": (suffix, True, ""),
        "tr": (translate, True, ""),
        "v": (verbosity, True, ""),
    }
    # 放弃枚举，采用程序判定
    allow_parameters = generate_allows()
    arg_list = sorted([arg for arg in args_dic.keys() if args_dic[arg][0]])
    arg_str = ".".join([arg for arg in arg_list])
    select_arg_str = ".".join([arg for arg in arg_list if arg not in ["d", "v", "sf", "pf", "p", "c", "l"]])
    error_list = [k for k, v in args_dic.items() if not v[1]]
    if debug:
        print(select_arg_str, translate_arr(*arg_list))
    # 参数检查发现错误
    if len(error_list) > 0:
        print("error", error_list)
        print([args_dic[err] for err in error_list])
        sys.exit(0)
    # 翻译字幕
    # 翻译字幕指定文件夹
    if arg_str not in allow_parameters.keys():
        print("不允许的参数")
        print("当前参数为", arg_str)
        print("允许的参数为:")
        for arg, introduce in allow_parameters.items():
            print(arg, introduce)
        sys.exit(1)
    # 翻译字幕
    if select_arg_str == "s.tr" or select_arg_str == "s.t.tr" or select_arg_str == "r.s.tr" or select_arg_str == "r.s.t.tr":
        translate_count = translate_subtitles(subtitles_path=subtitle, target_path=target_path, reverse=reverse)
        print("共翻译成功{}个".format(translate_count))
    # 移动bd媒体文件 根据数量自适应
    elif select_arg_str == "b.t":
        print("数量匹配")
        # 提取目标bd文件到目标位置 指定数量
        move_bd_to_target(target_path, prefix, suffix, only_print, reverse, hardlink, *bd_path)
    elif select_arg_str == "b.f.n.t" or select_arg_str == "b.f.n.r.t":
        print("数量匹配")
        # 提取目标bd文件到目标位置 指定数量
        move_bd_to_target_force_by_num(target_path, prefix, suffix, number, only_print, reverse, hardlink, *bd_path)
    # 移动媒体文件 根据数量和强制指定每个文件夹数量
    elif select_arg_str in ["b.e.f.t", "b.e.f.n.t"]:
        print("数量,每个匹配")
        # 提取目标bd文件到目标位置 指定每个，可选总数
        move_bd_to_target_force_by_each(target_path, prefix, suffix, number, each, only_print, hardlink, *bd_path)
    # 移动媒体文件 根据数量强制匹配
    elif select_arg_str in ["b.s", "b.f.s", "b.e.f.s", "b.s.t", "b.f.s.t", "b.e.f.s.t", "b.f.r.s", "b.f.r.s.t"]:
        print("匹配原盘")
        match_bd_subtitles(subtitle, target_path, prefix, suffix, each, force, only_print, copy_subtitle, reverse,
                           hardlink, *bd_path)
    elif select_arg_str in ["m.s", "m.s.t"]:
        print("匹配媒体")
        match_media_subtitles(media_path, subtitle, target_path, prefix, suffix, only_print, copy_subtitle, hardlink)
    else:
        print(select_arg_str, translate_arr(*arg_list))
        print("出现违规参数，程序错误")
        sys.exit(0)
