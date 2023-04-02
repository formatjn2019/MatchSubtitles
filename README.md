# MatchSubtitles

将外挂字幕文件和媒体文件进行匹配，省去手动批量重命名的工作.
(大概相当于一个自带规则的更名器吧)
主要是匹配原盘和字幕，一般媒体也附带可以匹配。
附带提取剧集文件到指定文件夹和简繁转换功能。

linux有两个，注意cpu架构

#### 使用方式
##### 打包好的文件：

`二进制文件名 参数`

如windows  `.\match_subtitles.exe -s . -tr`  翻译当前目录下的所有字幕文件

##### 源码

系统安装python3

pip安装 argparse : `pip install argparse`

使用： `python ./match_subtitle.py 参数`

#### 示例

1. `match_subtitles -s 字幕目录 -tr` 翻译并替换原文件
2. `match_subtitles -s 字幕目录 -m 视频目录` 匹配字幕文件到视频目录
3. `match_subtitles -s 字幕目录 -b 原盘目录` 匹配字幕文件到原盘目录
4. `match_subtitles -s 字幕目录 -b 原盘目录 -f` 强制匹配字幕文件到原盘目录。
5. `match_subtitles -s 字幕目录 -b 原盘目录 -f -r` 强制匹配字幕文件到原盘目录，翻转。
6. `match_subtitles -s 字幕目录 -b 原盘目录 -f -e 每个光盘数量` 强制匹配字幕文件到原盘目录
7. `match_subtitles -m 原盘目录 -t 目标目录 -f -n 文件数量` 不使用字幕，指定数量匹配，对应不带字幕的示例4
8. `match_subtitles -m 原盘目录 -t 目标目录 -f -n 文件数量 -r` 不使用字幕，指定数量匹配,翻转，对应不带字幕的示例5
9. `match_subtitles -m 原盘目录 -t 目标目录 -f -n 文件数量 -e 每个数量` 不使用字幕，指定数量和每个匹配，对应不带字幕的示例6

#### 使用说明 
[github源码页面](https://github.com/formatjn2019/myblog/blob/main/docs/%E5%B0%8F%E7%A8%8B%E5%BA%8F/%E5%AD%97%E5%B9%95%E5%8C%B9%E9%85%8D%E5%B0%8F%E7%A8%8B%E5%BA%8F.md)
[博客页面](http://blog.zuixue.site/%E5%B0%8F%E7%A8%8B%E5%BA%8F/%E5%AD%97%E5%B9%95%E5%8C%B9%E9%85%8D%E5%B0%8F%E7%A8%8B%E5%BA%8F.html)



版本说明

v 0.0.1 基本功能完成
基本集数可匹配
比如 原盘匹配
6光盘11集 可以匹配 2,2,2,2,2,1
7光盘12集 可匹配 2,2,2,2,2,2,0
8光盘25集 可匹配 3,3,3,3,3,3,3,4

v 0.0.2 更新功能
增加反向集数比较的匹配
如原盘匹配 强制模式 (加 `-r` 参数)
6光盘13集 可匹配 2,2,2,2,2,3 与 6光盘13集 可匹配 3,2,2,2,2,2
增加简中转繁中 同样需要加 `-r` 参数
