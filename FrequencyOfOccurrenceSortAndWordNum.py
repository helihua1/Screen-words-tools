import jieba
from collections import defaultdict
import pandas as pd
import numpy as np
from tqdm import tqdm


def preprocess_text(text):
    """预处理文本：分词并保留2字及以上词语"""
    if not isinstance(text, str):
        text = str(text)
    return [word for word in jieba.cut(text) if len(word) >= 2]


def calculate_advanced_weights(sentences,rate):
    """改进版权重计算：考虑词长加成"""
    # 统计词频和记录词长
    word_stats = defaultdict(lambda: {'count': 0, 'length': 0})

    # 第一次遍历：收集词频和词长信息
    for sentence in tqdm(sentences, desc="构建词库"):
        words = preprocess_text(sentence)
        for word in words:
            word_stats[word]['count'] += 1
            word_stats[word]['length'] = len(word)  # 记录词长

    # 计算带词长加权的有效词频
    weighted_word_freq = {}
    for word, stats in word_stats.items():
        # 权重 = 词频 × (2^(词长-2))
        # 例：2字词权重=词频×1，3字词=词频×2，4字词=词频×4
        weight = stats['count'] * (rate ** (stats['length'] - 2))
        weighted_word_freq[word] = weight

    # 第二次遍历：计算句子权重
    sentence_records = []
    for sentence in tqdm(sentences, desc="计算权重"):
        words = preprocess_text(sentence)
        if not words:
            sentence_records.append({
                'sentence': sentence,
                'keyword': '',
                'weight': 0,
                'max_word_length': 0
            })
            continue

        # 找出权重最高的词
        max_weight = 0
        best_word = ""
        for word in words:
            if weighted_word_freq[word] > max_weight:
                max_weight = weighted_word_freq[word]
                best_word = word

        sentence_records.append({
            'sentence': sentence,
            'keyword': best_word,
            'weight': max_weight,
            'max_word_length': len(best_word) if best_word else 0
        })

    return pd.DataFrame(sentence_records), weighted_word_freq


def sort_sentences(df):
    """多级排序：权重降序 > 词长降序 > 关键词字母序"""
    return df.sort_values(
        by=['weight', 'max_word_length', 'keyword'],
        ascending=[False, False, True]
    )


def main(input_path, output_path,rate):
    """主处理函数"""
    # 读取数据（假设第一列是文本）
    df_input = pd.read_excel(input_path, header=None)
    sentences = df_input.iloc[:, 0].astype(str).tolist()

    # 计算权重并排序
    result_df, _ = calculate_advanced_weights(sentences,rate)
    sorted_df = sort_sentences(result_df)

    # 输出结果（保留原始句子+关键词+权重）
    sorted_df[['sentence', 'keyword', 'weight']].to_excel(
        output_path, index=False, header=['句子', '关键词', '权重']
    )
    print(f"处理完成，结果已保存到 {output_path}")


if __name__ == "__main__":
    jieba.initialize()
    input_excel = r'D:\sort\A.xlsx'
    rateInput = 10
    print('倍率为' + str(rateInput))
    rate = rateInput * 2 #倍率在此处输入
    output_excel = fr'D:\sort\sorted_by_Frequency_AndWordNum{rateInput}X.xlsx'
    main(input_excel, output_excel,rate)