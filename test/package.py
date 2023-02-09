import sys
import argparse

parser = argparse.ArgumentParser(description="used for test")
media_group = parser.add_mutually_exclusive_group()

# 原盘文件路径
media_group.add_argument('--bdmv', '-b', action='append', dest='bd_path', help=('Blu-ray Disc file path'))
# 字幕文件夹
parser.add_argument('--captions', '-c', dest='captions', help='Path of subtitles')
# 调试
parser.add_argument('--debug', '-d', action='store_true', help='debug', default=False)
# 每个光盘文件夹有效媒体的数量
parser.add_argument('--each', '-e', dest='each', type=int, help='Number of media files in each')
# 强制模式
parser.add_argument('--force', '-f', action='store_true', dest='force', help='Forced mode', default=False)
# 数量
parser.add_argument('--num', '-n', dest='number', type=int, help='number of media')
# 前缀
parser.add_argument('--prefix', '-p', dest='prefix', help='File name prefix')
# 后缀
parser.add_argument('--suffix', '-s', dest='suffix', help='File name suffix')
# 翻译
parser.add_argument('--translate', '-t', action='store_true', help='Translate subtitles', default=False)
# 版本
parser.add_argument('--version', '-V', action='version', version='%(prog)s version : v 0.01', help='Show the version')
# 详细
parser.add_argument('--verbosity', '-v', action='store_true', help='Increase output verbosity', default=False)
# 通用媒体文件路径
media_group.add_argument('--media', '-m', action='append', dest='media_path', help=('Media file path'))

if __name__ == '__main__':
    args = parser.parse_args()
    print(type(args))
    if args.bd_path:
        print("原盘路径开启")
    if args.captions:
        print("字幕开启")
    if args.debug:
        print("调试开启")
    if args.each:
        print("每个文件开启")
    if args.force:
        print("强制模式开启")
    if args.media_path:
        print("媒体开启")
    if args.number:
        print("数量开启")
    if args.prefix:
        print("前缀开启")
    if args.suffix:
        print("后缀开启")
    if args.translate:
        print("翻译开启")
    if args.verbosity:
        print("详细信息开启")

    print(args)
    print(sys.argv)
    print(sys.orig_argv)
