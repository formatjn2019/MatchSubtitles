import math
import os
import shutil


# 为媒体文件添加字幕
# 注 多次运行会进行字幕的覆盖
def add_subtitle_for_media(media_subtitle_dic: dict, only_show: bool = True) -> int:
    replace_count = 0
    subtitle_set = set()
    for media_path, subtitles in media_subtitle_dic.items():
        print(media_path)
        replace_count += 1
        media_dir = os.path.dirname(media_path)
        media_name = os.path.basename(media_path)
        media_name = media_name[:media_name.index(".")]
        order = 0
        for subtitle_path in subtitles:
            subtitle_name = os.path.basename(subtitle_path)
            subtitle_suffix = subtitle_name[subtitle_name.find(".") + 1:]
            new_subtitle_path = os.path.join(media_dir, ".".join([media_name, subtitle_suffix]))
            while new_subtitle_path in subtitle_set:
                # 当字幕已存在时，重新生成字幕名
                new_subtitle_path = os.path.join(media_dir, ".".join([media_name, str(order), subtitle_suffix]))
                order += 1
            else:
                subtitle_set.add(new_subtitle_path)
            if only_show:
                print(subtitle_path, "----->", new_subtitle_path)
            else:
                print(subtitle_path, "已替换为-->", new_subtitle_path)
                shutil.copyfile(subtitle_path, new_subtitle_path)
    return replace_count


# 将全部文件移动到新路径
def move_media_subtitle_to_new_path(media_subtitle_dic: dict, order_media_dic: dict, target_dir: str, prefix="",
                                    suffix="",
                                    only_show: bool = True) -> int:
    result = 0
    move_dict = {}
    for order, media_path in order_media_dic.items():
        # 格式化，根据剧集数量计算格式化字符长度
        name = "{}{:0>{}d}{}".format(prefix, order, math.ceil(math.log10(len(order_media_dic))), suffix)
        media_name = os.path.basename(media_path)
        # 媒体名称
        move_dict[os.path.join(target_dir, "{}{}".format(name, media_name[media_name.index("."):]))] = media_path
        order = 1
        for subtitle_path in media_subtitle_dic[media_path]:
            subtitle_name = os.path.basename(subtitle_path)
            new_subtitle_name = "{}{}".format(name, subtitle_name[subtitle_name.index("."):])
            while new_subtitle_name in move_dict:
                # 当字幕已存在时，重新生成字幕名
                new_subtitle_name = ".".join([name, str(order), subtitle_name[subtitle_name.index("."):]])
                order += 1
            else:
                # 字幕名称
                move_dict[os.path.join(target_dir, new_subtitle_name)] = subtitle_path
        result += 1

    for target_path, source_path in move_dict.items():
        if only_show:
            print(source_path, "----->", target_path)
        else:
            shutil.move(source_path, target_path)
            print(source_path, "移动至-->", target_path)
    return result
