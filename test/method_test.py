import subprocess
import time
import unittest
# import moviepy

def video_duration_1(filename):
    start = time.time()
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    end = time.time()
    spend = end - start
    print("获取视频时长方法1耗时：", spend)
    return float(result.stdout)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        video_duration_1("00007.m2ts")
        # self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
