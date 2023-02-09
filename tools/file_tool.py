import math
import os
import shutil


# 为媒体文件添加字幕
# 注 多次运行会进行字幕的覆盖
def add_caption_for_media(media_caption_dic: dict, only_show: bool = True) -> int:
    replace_count = 0
    caption_set = set()
    for media_path, captions in media_caption_dic.items():
        print(media_path)
        replace_count += 1
        media_dir = os.path.dirname(media_path)
        media_name = os.path.basename(media_path)
        media_name = media_name[:media_name.index(".")]
        order = 0
        for caption_path in captions:
            caption_name = os.path.basename(caption_path)
            caption_suffix = caption_name[caption_name.find(".") + 1:]
            new_caption_path = os.path.join(media_dir, ".".join([media_name, caption_suffix]))
            while new_caption_path in caption_set:
                # 当字幕已存在时，重新生成字幕名
                new_caption_path = os.path.join(media_dir, ".".join([media_name, str(order), caption_suffix]))
                order += 1
            else:
                caption_set.add(new_caption_path)
            if only_show:
                print(caption_path, "----->", new_caption_path)
            else:
                print(caption_path, "已替换为-->", new_caption_path)
                shutil.copyfile(caption_path, new_caption_path)
    return replace_count


# 将全部文件移动到新路径
def move_media_caption_to_new_path(media_caption_dic: dict, order_media_dic: dict, target_dir: str, prefix="",
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
        for caption_path in media_caption_dic[media_path]:
            caption_name = os.path.basename(caption_path)
            new_caption_name = "{}{}".format(name, caption_name[caption_name.index("."):])
            while new_caption_name in move_dict:
                # 当字幕已存在时，重新生成字幕名
                new_caption_name = ".".join([name, str(order), caption_name[caption_name.index("."):]])
                order += 1
            else:
                # 字幕名称
                move_dict[os.path.join(target_dir, new_caption_name)] = caption_path
        result += 1

    for target_path, source_path in move_dict.items():
        if only_show:
            print(source_path, "----->", target_path)
        else:
            shutil.move(source_path, target_path)
            print(source_path, "移动至-->", target_path)
    return result
