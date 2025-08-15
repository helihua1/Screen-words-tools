import jieba
from rapidfuzz import fuzz
from pypinyin import lazy_pinyin
from functools import lru_cache
from joblib import Parallel, delayed
import jieba
import sys, jieba
if __name__ == "__main__":
    # s1和s2顺序无关
    # 53
    print(fuzz.partial_ratio( "宁波博润医院在哪里","宁波鄞州博润皮肤病医院"))
    # 60 适合去除关键词的匹配
    print(fuzz.token_set_ratio("宁波鄞州博润皮肤病医院", "宁波博润医院在哪里"))
    # 70
    print(fuzz.token_set_ratio( "宁波博润医院","宁波鄞州博润皮肤病医院"))
    # 53
    print(fuzz.token_set_ratio("宁波博润", "宁波鄞州博润皮肤病医院"))
    # 66 适合子集匹配
    print(fuzz.partial_ratio("宁波博润", "宁波鄞州博润皮肤病医院"))
    # 61
    print(fuzz.partial_ratio("宁波博润在哪里", "宁波鄞州博润皮肤病医院"))

    print(jieba.__version__)  # 确认版本是否支持 lcut_for_search



    print(sys.executable)  # 当前 Python 解释器路径
    print(jieba.__file__)  # jieba 模块所在文件夹
    print(jieba.__version__)  # jieba 版本

    from utils import chinese_segment, get_pinyin


    # 用户输入的：宁波博润，处理成：[宁波,博润],在关键词‘宁波鄞州博润皮肤病医院’中，匹配成功！返回关键词。
    print (chinese_segment('宁波鄞州博润皮肤病医院'))
    print(chinese_segment('雷公藤'))

    print(' '.join(lazy_pinyin('宁波鄞州博润皮肤病医院')))

