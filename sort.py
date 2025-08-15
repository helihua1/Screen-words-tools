import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import jieba
import openpyxl
import numpy as np


def preprocess_text(text):
    """预处理中文文本：分词并去除标点符号"""
    # 使用jieba进行分词（兼容旧版本）
    words = list(jieba.cut(text))  # 使用jieba.cut并转换为list
    # 过滤掉标点符号和非中文字符
    filtered_words = [word for word in words if '\u4e00' <= word <= '\u9fff']
    return ' '.join(filtered_words)


def cluster_sentences(sentences, n_clusters=10):
    """使用TF-IDF和K-means对句子进行聚类"""
    # 预处理所有句子
    processed_sentences = [preprocess_text(s) for s in sentences]

    # 创建TF-IDF向量器
    vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(' '))
    X = vectorizer.fit_transform(processed_sentences)

    # 使用K-means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)

    # 计算每个句子与其聚类中心的余弦相似度
    distances = kmeans.transform(X)

    return kmeans.labels_, distances


def sort_within_clusters(sentences, labels, distances):
    """在每个聚类内部根据与中心的距离排序"""
    # 创建一个包含句子、标签和距离的DataFrame
    df = pd.DataFrame({
        'sentence': sentences,
        'cluster': labels,
        'distance': np.min(distances, axis=1)
    })

    # 按聚类标签和距离排序
    df_sorted = df.sort_values(by=['cluster', 'distance'])

    return df_sorted['sentence'].tolist()


def main():
    # 读取Excel文件
    input_path = r'D:\sort\A2.xlsx'
    output_path = r'D:\sort\sorted2.xlsx'

    try:
        # 读取Excel文件，假设数据在第二列（索引为1）
        df = pd.read_excel(input_path, header=None)
        df = df.fillna('')  # 将NaN替换为空字符串df = df.fillna('')  # 将NaN替换为空字符串
        # 确保所有数据转换为字符串（包括数字）
        sentences = df.iloc[:, 0].astype(str).tolist()  # 第一列数据，强制转换为字符串
        # sentences = df.iloc[:, 0].tolist()  # 第一列数据

        # 确定聚类数量（根据句子数量的平方根）
        n_clusters = int(np.sqrt(len(sentences)))
        n_clusters = max(5, min(n_clusters, 50))  # 限制在5-50之间

        # 聚类和排序
        labels, distances = cluster_sentences(sentences, n_clusters=n_clusters)
        sorted_sentences = sort_within_clusters(sentences, labels, distances)

        # 创建新的DataFrame并保存
        result_df = pd.DataFrame({'Sorted Sentences': sorted_sentences})
        result_df.to_excel(output_path, index=False)

        print(f"排序完成，结果已保存到 {output_path}")

    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    # 初始化jieba（旧版本可能不需要这行）
    jieba.initialize()  # 如果这行报错，可以注释掉
    main()