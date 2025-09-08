import pandas as pd
from rapidfuzz import fuzz
from pypinyin import lazy_pinyin
from functools import lru_cache
from joblib import Parallel, delayed
import jieba

'''
此功能用rag语义匹配替代，暂时不用
'''

def chinese_segment(text):
    # 输入："宁波鄞州博润皮肤病医院" 输出：['宁波', '鄞州', '博润', '皮肤', '医院']
    # return [w for w in jieba.lcut_for_search(text) if len(w) >= 2]
    return [w for w in jieba.lcut_for_search(text) ]


def get_pinyin(text):
    return ' '.join(lazy_pinyin(text))#输入： 宁波医院 输出：ningboyiyuan

def fast_filter(user_input, keywords):
    words = chinese_segment(user_input)
    # 用户输入的：宁波博润，处理成：[宁波,博润],在关键词‘宁波鄞州博润皮肤病医院’中，匹配成功！返回关键词。
    return [kw for kw in keywords if any(word in kw for word in words)]


def fuzzy_match_optimized(user_input, keywords, pinyin_keywords, threshold=60):
    # 阶段1：快速过滤
    candidates = fast_filter(user_input, keywords)
    if not candidates:
        return None
    # 阶段2：精准匹配
    for kw in candidates:
        # score = max(
        #     fuzz.partial_ratio(kw, user_input),
        #     fuzz.token_set_ratio(kw, user_input)
        # )
        # if score >= threshold:
        #     return [kw,score,'中文匹配']
        # 拼音匹配
        score = fuzz.ratio(pinyin_keywords[kw], get_pinyin(user_input))
        if score >= threshold:
            return [kw,score,'拼音匹配']
    return None

def process_excel_files():
    # 文件路径设置
    sorted_file_path = r"D:\sort\A.xlsx"
    priority_file_path = r"D:\sort\确定可以保存的词.xlsx"
    output_file_path = r"D:\sort\sort_save_fuzz.xlsx"

    # 读取sorted.xlsx中的句子（第1列）
    sorted_df = pd.read_excel(sorted_file_path, header=None, usecols=[0])
    one_col1 = sorted_df.stack().tolist()

    # 确定可以保存的词.xlsx中的句子（第4,8列）
    priority_df = pd.read_excel(priority_file_path, header=None, usecols=[3,7])
    one_col2 = priority_df.stack().tolist()
    # 在读取关键词后添加数据清洗
    one_col2 = [str(kw) for kw in one_col2 if kw and str(kw).strip()]  # 转为字符串并过滤空值


    # 预处理关键词拼音
    keywords = one_col2  # 关键词
    pinyin_keywords = {kw: ''.join(lazy_pinyin(str(kw))) for kw in keywords}

    user_inputs = one_col1  # 5万句
    results = Parallel(n_jobs=-1)(
        delayed(fuzzy_match_optimized)(input_, keywords, pinyin_keywords)
        for input_ in user_inputs
    )
    # 将结果转换为DataFrame
    output_data = []
    for input_, result in zip(user_inputs, results):
        if result:  # 如果有匹配结果
            kw, score, match_type = result
            output_data.append({
                'input_': input_,
                'kw': kw,
                'score': score,
                'match_type': match_type
            })
        else:  # 如果没有匹配结果
            output_data.append({
                'input_': input_,
                'kw': None,
                'score': None,
                'match_type': None
            })

    # 创建DataFrame
    df = pd.DataFrame(output_data, columns=['input_', 'kw', 'score', 'match_type'])

    # 保存到Excel
    df.to_excel(output_file_path, index=False)


# 批量并行匹配
if __name__ == "__main__":
    # 初始化jieba（提高首次分词速度）
    jieba.initialize()
    process_excel_files()

