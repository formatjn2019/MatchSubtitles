import collections

TRANSLATE_DIC = collections.OrderedDict()


# 获取简繁映射字典
def init_translate_dic(filepath: str):
    with open(filepath, "r", encoding="utf8") as f:
        rules = f.readlines()
        for rule in rules:
            context = rule.split()
            if len(context) == 2:
                TRANSLATE_DIC[context[0]] = context[1]


# 翻译
def translate_file(file_path: str):
    with open(file_path, "wr", encoding="utf8") as f:
        context = file_path
        con


if __name__ == '__main__':
    init_translate_dic("../resource/rule.txt")
    print(len(TRANSLATE_DIC))
    for k, v in TRANSLATE_DIC.items():
        print(k, v)
