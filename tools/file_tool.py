import os
import shutil

from setting import setting
from utils import file_util


# 移动,复制文件，统一处理
def move_copy_files(source_target_dic: dict, only_show=False, copy_file=False) -> (int, int):
    print(only_show)
    print(len(source_target_dic))
    succeed, error = 0, 0
    for source_path, target_path in source_target_dic.items():
        if only_show:
            print(source_path, "----->", target_path)
        else:
            try:
                if copy_file:
                    shutil.copyfile(source_path, target_path)
                else:
                    shutil.move(source_path, target_path)
            except IOError as e:
                if setting.debug:
                    print(source_path, target_path, e)
                error += 1
                print(source_path, "----->", target_path, "error")
            else:
                succeed += 1
                print(source_path, "----->", target_path, "succeed")
    print("共移动{}个文件,其中成功{}个,失败{}个".format(succeed + error, succeed, error))
    return succeed, error


# 为媒体文件添加字幕
# 注 多次运行会进行字幕的覆盖
def add_subtitle_for_media(media_subtitle_dic: dict, only_show: bool = True, copy_subtitle=False) -> int:
    subtitle_set = set()
    subtitle_source_target_dic = {}
    for media_path, subtitles in media_subtitle_dic.items():
        media_dir = os.path.dirname(media_path)
        media_name = file_util.get_file_name(media_path)
        order = 0
        for subtitle_path in subtitles:
            subtitle_suffix = file_util.get_file_extension(subtitle_path)
            new_subtitle_path = os.path.join(media_dir, ".".join([media_name, subtitle_suffix]))
            while new_subtitle_path in subtitle_set:
                # 当字幕已存在时，重新生成字幕名
                new_subtitle_path = os.path.join(media_dir, ".".join([media_name, str(order), subtitle_suffix]))
                order += 1
            else:
                subtitle_set.add(new_subtitle_path)
            subtitle_source_target_dic[subtitle_path] = new_subtitle_path
    succeed, _ = move_copy_files(subtitle_source_target_dic, only_show, copy_subtitle)
    # print(len(subtitle_source_target_dic))
    return len(media_subtitle_dic) if only_show else succeed


# 将全部文件移动到新路径
def move_media_subtitle_to_new_path(media_subtitle_dic: dict, order_media_dic: dict, target_dir: str, prefix="",
                                    suffix="", only_show: bool = True, copy_subtitle=False) -> int:
    media_dic, subtitle_dic, subtitles_set = {}, {}, set()
    for order, media_path in order_media_dic.items():
        # 格式化，根据剧集数量计算格式化字符长度
        name = file_util.generate_filename(size=len(order_media_dic), prefix=prefix, suffix=suffix, order=order)
        media_dic[media_path] = os.path.join(target_dir,
                                             name + "." + file_util.get_file_extension(file_path=media_path))
        order = 1
        for subtitle_path in media_subtitle_dic[media_path]:
            extension = file_util.get_file_extension(subtitle_path)
            new_subtitle_name = ".".join([name, extension])
            while new_subtitle_name in subtitles_set:
                # 当字幕已存在时，重新生成字幕名
                new_subtitle_name = ".".join([name, str(order), extension])
                order += 1
            else:
                # 字幕名称加入集合
                subtitles_set.add(new_subtitle_name)
                subtitle_dic[subtitle_path] = os.path.join(target_dir, new_subtitle_name)

    move_copy_files(source_target_dic=subtitle_dic, only_show=only_show, copy_file=copy_subtitle)
    successes, _ = move_copy_files(source_target_dic=media_dic, only_show=only_show, copy_file=False)
    return successes
