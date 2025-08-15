import jieba
from collections import Counter
import pandas as pd
import numpy as np
from tqdm import tqdm  # 进度条


def preprocess_text(text):
    """预处理文本：分词并保留2字及以上词语"""
    if not isinstance(text, str):
        text = str(text)
    words = [word for word in jieba.cut(text) if len(word) >= 2]
    return words


def calculate_sentence_weights(sentences):
    """计算句子权重"""
    # 统计所有2字及以上词语的频率
    all_words = []
    for sentence in tqdm(sentences, desc="分词处理"):
        all_words.extend(preprocess_text(sentence))
    word_freq = Counter(all_words)

    # 计算每个句子的最高权重
    sentence_weights = []
    sentence_keywords = []

    for sentence in tqdm(sentences, desc="计算权重"):
        words = preprocess_text(sentence)
        if not words:
            # 如果没有2字及以上词语，权重为0
            sentence_weights.append(0)
            sentence_keywords.append("")
            continue

        # 找出句子中权重最高的词
        max_weight = 0
        best_word = ""
        for word in words:
            if word_freq[word] > max_weight:
                max_weight = word_freq[word]
                best_word = word

        sentence_weights.append(max_weight)
        sentence_keywords.append(best_word)

    return sentence_weights, sentence_keywords, word_freq


def sort_sentences(sentences):
    """排序句子"""
    # 计算权重
    weights, keywords, _ = calculate_sentence_weights(sentences)

    # 创建DataFrame以便排序
    df = pd.DataFrame({
        'sentence': sentences,
        'keyword': keywords,
        'weight': weights
    })

    # 先按权重降序，再按关键词分组排序
    df_sorted = df.sort_values(
        by=['weight', 'keyword'],
        ascending=[False, True]
    )

    return df_sorted


def main(input_path, output_path):
    """主处理函数"""
    # 读取Excel文件
    df = pd.read_excel(input_path, header=None)
    sentences = df.iloc[:, 1].astype(str).tolist()  # 第二列

    # 处理排序
    result_df = sort_sentences(sentences)

    # 保存结果
    result_df.to_excel(output_path, index=False, header=['句子', '关键词', '权重'])
    print(f"处理完成，结果已保存到 {output_path}")


if __name__ == "__main__":
    # 初始化jieba
    jieba.initialize()

    # 文件路径
    input_excel = r'D:\sort\A去除银屑病牛皮癣.xlsx'  # 输入文件路径
    output_excel = r'D:\sort\sorted_by_Frequency.xlsx'  # 输出文件路径

    # 运行主程序
    main(input_excel, output_excel)