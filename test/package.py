import sys
import argparse

parser = argparse.ArgumentParser(description="used for test")

parser.add_argument('--version', '-V', action='version',
                    version='%(prog)s version : v 0.01',
                    help='show the version')

parser.add_argument('--visual', '-v', action='store_false',
                    help='show the version',
                    default=False)

parser.add_argument('--debug', '-d', action='store_true',
                    help='show the version',
                    default=False)

parser.add_argument('--translate', '-t', action='store_true',
                    help=('Translate subtitles'),
                    default=False)

parser.add_argument('--subtitle', '-s',
                    dest='subtitle',
                    help=('Path of subtitles'),
                    )

parser.add_argument('--media', '-m', action='append',
                    dest='files',
                    help=('additional yaml configuration files to use'),
                    type=argparse.FileType('rb'))

parser.add_argument('--bdmv', '-b', action='append',
                    dest='files',
                    help=('additional yaml configuration files to use'),
                    type=argparse.FileType('rb'))

#
# def main_single(name, args):
#     print("name: ", name)
#     print("args: ", args)
#     print("I am main_single")

#
#
#
# parser_single = subparsers.add_parser('single', help='run a single module')
#
# # 对single 子解析器添加 action 函数。
# parser_single.set_defaults(action=('single', main_single))
#
# # require=True，是说如果命令行指定了single解析器，就必须带上 --name 的参数。
# parser_single.add_argument("--name", '-n', action="store",
#                            help="module name to run",
#                            required=True)
#
# args = parser.parse_args()
#
# (name, functor) = args.action
# if name in ["single"]:
#     functor(name, args)

if __name__ == '__main__':
    args = parser.parse_args()
    print(type(args))
    print(args)
    print(sys.argv)
    print(sys.orig_argv)
