from functools import lru_cache
import jieba
from pypinyin import lazy_pinyin


@lru_cache(maxsize=10000)
def chinese_segment(text):
    # 输入："宁波鄞州博润皮肤病医院" 输出：['宁波', '鄞州', '博润', '皮肤', '医院']
    # return [w for w in jieba.lcut_for_search(text) if len(w) >= 2]
    return [w for w in jieba.lcut_for_search(text) ]

@lru_cache(maxsize=10000)
def get_pinyin(text):
    return ' '.join(lazy_pinyin(text))#输入： 宁波医院 输出：ningboyiyuan

