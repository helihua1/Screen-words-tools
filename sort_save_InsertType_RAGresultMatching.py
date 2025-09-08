import re

import pandas as pd
import os

'''
PRIORITY_FILE_PATH 表格格式 :疾病	栏目	素材类型	关键词
SORTED_FILE_PATH 表格格式 :分数 rag的匹配结果 用户输入
rag的匹配结果和PRIORITY_FILE_PATH表格中的关键词匹配，匹配成功则将句子保存到OUTPUT_FILE_PATH表格的后几列中。未匹配的句子保存到OUTPUT_FILE_PATH表格的第1列。
OUTPUT_FILE_PATH 表格格式 :未匹配的句子	|	匹配到的句子和分数等
'''

def process_excel_files():
    # 文件路径设置
    sorted_file_path = r"D:\sort\rag.xlsx"
    priority_file_path = r"D:\sort\RAG数据库同步.xlsx"
    output_file_path = r"D:\sort\rag结果_sort_save_InsertType.xlsx"

    try:
        # 读取sorted.xlsx中的前三列数据
        sorted_df = pd.read_excel(sorted_file_path, header=None, usecols=[0, 1, 2])
        
        # 获取前三列数据
        scores = sorted_df[0].tolist()  # 第0列: score
        sentences = sorted_df[1].tolist()  # 第1列: sentences
        user_inputs = sorted_df[2].tolist()  # 第2列: user_input

        # 读取优先聚合.xlsx中的词（第4列和第8列）及其前3列属性
        priority_df = pd.read_excel(priority_file_path, header=None, usecols=[0, 1, 2, 3, 4, 5, 6, 7])

        # 存储第4列关键词及其属性（前3列）
        priority1_words = []
        priority1_attrs = {}  # 键:关键词, 值:属性列表[attr0, attr1, attr2]
        # 存储第8列关键词及其属性（前3列）
        priority2_words = []
        priority2_attrs = {}  # 键:关键词, 值:属性列表[attr4, attr5, attr6]

        # 提取关键词及其对应的属性
        for idx, row in priority_df.iterrows():
            # 处理第4列（索引3）的关键词及其属性
            word1 = row[3]
            if not pd.isna(word1):
                priority1_words.append(word1)
                # 获取前3列属性（索引0、1、2）
                priority1_attrs[word1] = [row[0], row[1], row[2]]

            # 处理第8列（索引7）的关键词及其属性
            word2 = row[7]
            if not pd.isna(word2):
                priority2_words.append(word2)
                # 获取前3列属性（索引4、5、6）
                priority2_attrs[word2] = [row[4], row[5], row[6]]

        # 用于存储匹配到的句子及对应的关键词、属性和原始数据
        matched_dict = {}  # 键:关键词, 值:列表，每个元素为[句子, score, user_input]
        remaining_user_inputs = []  # 存储未匹配的user_input

        # 遍历所有句子，检查是否包含优先聚合词并记录匹配的关键词
        for i, sentence in enumerate(sentences):
            if pd.isna(sentence):  # 不对空值进行比对
                # 即使句子为空，也保留user_input
                if not pd.isna(user_inputs[i]):
                    remaining_user_inputs.append(user_inputs[i])
                continue

            matched_word = None
            # 先检查第4列优先级高的词
            for word in priority1_words:
                if str(word) in str(sentence):
                    matched_word = word
                    break

            # 如果没有匹配到第4列的词，检查第8列的词
            if matched_word is None:
                for word in priority2_words:
                    if str(word) in str(sentence):
                        matched_word = word
                        break

            # 处理匹配结果
            if matched_word is not None:
                # 将句子及其对应的score和user_input添加到对应关键词的列表中
                if matched_word not in matched_dict:
                    matched_dict[matched_word] = []
                matched_dict[matched_word].append([sentence, scores[i], user_inputs[i]])
            else:
                # 未匹配的句子，只保留user_input
                if not pd.isna(user_inputs[i]):
                    remaining_user_inputs.append(user_inputs[i])

        # 按关键词优先级顺序聚合句子及相关信息
        aggregated_data = []  # 每个元素: [attr1, attr2, attr3, 关键词, 句子, score, user_input]
        
        # 先处理第4列的关键词（按原顺序）
        for word in priority1_words:
            if word in matched_dict:
                # 获取该关键词对应的属性
                attrs = priority1_attrs[word]
                # 为每个匹配的句子添加属性、关键词、句子、score和user_input
                for match in matched_dict[word]:
                    aggregated_data.append([attrs[0], attrs[1], attrs[2], word, match[0], match[1], match[2]])
                del matched_dict[word]  # 避免重复处理

        # 再处理第8列的关键词（按原顺序）
        for word in priority2_words:
            if word in matched_dict:
                # 获取该关键词对应的属性
                attrs = priority2_attrs[word]
                # 为每个匹配的句子添加属性、关键词、句子、score和user_input
                for match in matched_dict[word]:
                    aggregated_data.append([attrs[0], attrs[1], attrs[2], word, match[0], match[1], match[2]])
                del matched_dict[word]

        # 准备构建结果DataFrame的数据
        max_length = max(len(aggregated_data), len(remaining_user_inputs))

        # 拆分聚合数据到各列
        agg_attr1 = [item[0] for item in aggregated_data] + [None] * (max_length - len(aggregated_data))
        agg_attr2 = [item[1] for item in aggregated_data] + [None] * (max_length - len(aggregated_data))
        agg_attr3 = [item[2] for item in aggregated_data] + [None] * (max_length - len(aggregated_data))
        agg_keywords = [item[3] for item in aggregated_data] + [None] * (max_length - len(aggregated_data))
        agg_sentences = [item[4] for item in aggregated_data] + [None] * (max_length - len(aggregated_data))
        agg_scores = [item[5] for item in aggregated_data] + [None] * (max_length - len(aggregated_data))
        agg_user_inputs = [item[6] for item in aggregated_data] + [None] * (max_length - len(aggregated_data))

        # 创建新的DataFrame，列分布：
        # 0: 未匹配的user_input
        # 1: 预留列
        # 2: 预留列
        # 3: 关键词属性1
        # 4: 关键词属性2
        # 5: 关键词属性3
        # 6: 匹配到的关键词
        # 7: 匹配到的句子
        # 8: 匹配到的score
        # 9: 匹配到的user_input
        result_data = {
            0: remaining_user_inputs + [None] * (max_length - len(remaining_user_inputs)),
            1: [None] * max_length,  # 预留列1
            2: [None] * max_length,  # 预留列2
            3: agg_attr1,  # 关键词属性1
            4: agg_attr2,  # 关键词属性2
            5: agg_attr3,  # 关键词属性3
            6: agg_keywords,  # 匹配到的关键词
            7: agg_sentences,  # 匹配到的句子
            8: agg_scores,  # 匹配到的score
            9: agg_user_inputs  # 匹配到的user_input
        }

        result_df = pd.DataFrame(result_data)

        # 保存结果到新的Excel文件
        result_df.to_excel(output_file_path, index=False, header=False)
        print(f"处理完成！结果已保存至：{output_file_path}")

    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")


if __name__ == "__main__":
    process_excel_files()