import collections

TRANSLATE_DIC = collections.OrderedDict()


# 获取简繁映射字典
# csv格式
def init_translate_dic(filepath: str, reverse: bool = False):
    try:
        with open(filepath, "r", encoding="utf8") as f:
            rules = f.readlines()
            for rule in rules:
                rule = rule.strip()
                context = rule.split(",")
                if len(context) == 2:
                    if reverse:
                        TRANSLATE_DIC[context[1]] = context[0]
                    else:
                        TRANSLATE_DIC[context[0]] = context[1]
    except IOError:
        print("加载翻译规则错误")


# 翻译
# 不指定保存路径则直接翻译原文
def translate_file(file_path: str, target_path: str = None) -> bool:
    try:
        if target_path is None:
            target_path = file_path
        with open(file_path, "r", encoding="utf8") as f:
            context = f.read()
            for tc, sc in TRANSLATE_DIC.items():
                context = context.replace(tc, sc)
            translated = context
        with open(target_path, "w", encoding="utf8") as f:
            f.write(translated)
    except IOError:
        print(file_path, "读写异常")
        return False
    else:
        return True
