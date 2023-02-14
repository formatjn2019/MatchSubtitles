import os


# 检查路径是否存在
def check_path(*paths: str, isdir: bool) -> (bool, str):
    for path in paths:
        if not os.path.exists(path):
            return False, "'{}' Path does not exist".format(path)
        elif os.path.isdir(path) != isdir:
            return False, "Folder path required" if isdir else "File path required"
    return True, ""


#


if __name__ == '__main__':
    print(check_path(".", "..", "../tools", isdir=True))
