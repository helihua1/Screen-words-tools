import re

import pandas as pd
import os


def process_excel_files():
    # 文件路径设置
    sorted_file_path = r"D:\sort\A.xlsx"
    priority_file_path = r"D:\sort\确定可以保存的词.xlsx"
    output_file_path = r"D:\sort\A_save.xlsx"

    try:
        # 读取sorted.xlsx中的句子（第1列）
        sorted_df = pd.read_excel(sorted_file_path, header=None, usecols=[0])


        sentences = sorted_df[0].tolist()  # 获取第1列所有句子

        # 读取优先聚合.xlsx中的词（第1列和第2列）
        priority_df = pd.read_excel(priority_file_path, header=None, usecols=[3, 7])


        priority1_words = priority_df[3].dropna().tolist()  # 第4列优先级高的词
        priority2_words = priority_df[7].dropna().tolist()  # 第8列优先级低的词

        # 用于存储匹配到的句子及对应的关键词
        matched_dict = {}  # 键:关键词, 值:该关键词匹配到的句子列表
        remaining_sentences = []

        # 遍历所有句子，检查是否包含优先聚合词并记录匹配的关键词
        for sentence in sentences:
            if pd.isna(sentence):  # 不对空值进行比对
                remaining_sentences.append(sentence)
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
                # 将句子添加到对应关键词的列表中
                if matched_word not in matched_dict:
                    matched_dict[matched_word] = []

                # 方法一：
                # 判断句子是否包含"治"字，如果是则插入列表开头，否则追加到末尾
                # re.escape(matched_word)对matched_word中的特殊字符进行转义
                # 为什么需要：正则表达式中有特殊含义的字符如. * ? + ^ $等，如果matched_word包含这些字符会被误认为是正则语法
                # 示例：
                # 输入：matched_word = "我?"
                # 输出：re.escape("我?") → "我\?"（问号被转义）
                #
                # .*的含义：
                # .：匹配任意单个字符（除换行符）
                # * ：匹配前面的字符0次或多次
                # .*组合：匹配任意长度的任意字符序列（包括空序列）
                # pattern = re.compile(f"{re.escape(str(matched_word))}.*治")  # 创建正则表达式模式对象#空单元格则 str(matched_word)是str(float('nan'))  # 结果为 'nan'
                # if pattern.search(sentence):  # 在句子中搜索该模式

                # 方法二：
                #直接判定句子中是否有治字
                # if "治" in str(sentence):
                #     matched_dict[matched_word].insert(0, sentence)  # 插入到列表开头
                # else:
                #     matched_dict[matched_word].append(sentence)  # 追加到列表末尾
                matched_dict[matched_word].append(sentence)  # 追加到列表末尾
            else:
                remaining_sentences.append(sentence)

        # 按关键词优先级顺序聚合句子（保持原优先级和原句相对顺序）
        aggregated_sentences = []
        # 先处理第一列的关键词（按原顺序）
        for word in priority1_words:
            if word in matched_dict:
                aggregated_sentences.extend(matched_dict[word])
                del matched_dict[word]  # 避免重复处理
        # 再处理第二列的关键词（按原顺序）
        for word in priority2_words:
            if word in matched_dict:
                aggregated_sentences.extend(matched_dict[word])
                del matched_dict[word]

        # 创建新的DataFrame，将聚合后的句子放在第4列（索引3）
        max_length = max(len(aggregated_sentences), len(remaining_sentences))
        result_data = {
            0: remaining_sentences + [None] * (max_length - len(remaining_sentences)),
            1: [None] * max_length,
            2: [None] * max_length,
            3: aggregated_sentences + [None] * (max_length - len(aggregated_sentences))
        }

        result_df = pd.DataFrame(result_data)

        # 保存结果到新的Excel文件
        result_df.to_excel(output_file_path, index=False, header=False)
        print(f"处理完成！结果已保存至：{output_file_path}")

    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")


if __name__ == "__main__":
    process_excel_files()
