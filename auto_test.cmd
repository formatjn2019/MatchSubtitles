@echo off
@REM 自动匹配模式6_11
python .\match_subtitles.py -p -b .\test_file\bdmv\6_11\ -s .\test_file\subtitle\6_11_subtitle -t .\test_file\target\bd_target
@REM 自动匹配模式6_12
python .\match_subtitles.py -p -b .\test_file\bdmv\6_12\ -s .\test_file\subtitle\6_12_subtitle -t .\test_file\target\bd_target
@REM 自动匹配模式6_13
python .\match_subtitles.py -p -b .\test_file\bdmv\6_13\ -s .\test_file\subtitle\6_13_subtitle -t .\test_file\target\bd_target
@REM 强制每个匹配模式7_12
python .\match_subtitles.py -p -f -e 2 -b .\test_file\bdmv\7_12\ -s .\test_file\subtitle\7_12_subtitle -t .\test_file\target\bd_target
@REM 强制每个匹配模式8_25
python .\match_subtitles.py -p -f -b .\test_file\bdmv\8_25\ -s .\test_file\subtitle\8_25_subtitle -t .\test_file\target\bd_target