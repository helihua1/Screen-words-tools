
import pandas as pd


def add_word_c_if_contains_pandas(file_a_path, file_b_path, output_path):

    # 读取B.xls中两个sheet的关键词
    df_related = pd.read_excel(file_b_path, sheet_name='related', header=None, usecols=[1])
    df_unrelated = pd.read_excel(file_b_path, sheet_name='unrelated', header=None, usecols=[1])

    # 提取关键词列表
    related_keywords = df_related[1].dropna().astype(str).tolist()
    unrelated_keywords = df_unrelated[1].dropna().astype(str).tolist()

    # 读取A.xls
    df_a = pd.read_excel(file_a_path, header=None)

    # 创建布尔掩码，查找related关键词
    mask_related = df_a[1].apply(lambda x: any(kw in x for kw in related_keywords))

    # 将匹配的关键词填入第0列（列索引0）
    def get_first_related_keyword(text):
        for kw in related_keywords:
            if kw in text:
                return kw
        return ""

    # 将related关键词填入第0列
    df_a.loc[mask_related, 0] = df_a.loc[mask_related, 1].apply(get_first_related_keyword)

    # 匹配unrelated关键词
    mask_unrelated = df_a[1].apply(lambda x: any(kw in x for kw in unrelated_keywords))

    # 1️⃣ 将匹配的长尾词放到第4列
    df_a.loc[mask_unrelated, 3] = df_a.loc[mask_unrelated, 1]

    # 2️⃣ 删除第1列中这些匹配词
    df_a.loc[mask_unrelated, 1] = pd.NA

    # 3️⃣ “压缩”第1列中的非空值：移除空值后重排
    compressed_col_1 = df_a[1].dropna().reset_index(drop=True)

    # 4️⃣ 用重排后的内容替换整列，再补齐DataFrame长度
    df_a[1] = pd.NA  # 清空原列
    df_a.loc[:len(compressed_col_1) - 1, 1] = compressed_col_1

    # 保存结果
    df_a.to_excel(output_path, index=False, header=False)

    # df_a.loc[mask_related, 0] = df_a.loc[mask_related, 1].apply(get_first_related_keyword)
    #
    # # 创建布尔掩码，查找unrelated关键词
    # mask_unrelated = df_a[1].apply(lambda x: any(kw in x for kw in unrelated_keywords))
    #
    # # 把匹配到的长尾词（第1列）迁移到第4列（索引3），然后可以根据需要清空第1列
    # df_a.loc[mask_unrelated, 3] = df_a.loc[mask_unrelated, 1]
    # df_a.loc[mask_unrelated, 1] = ""  # 如果不想清空第1列可删去这行
    #
    # # 保存结果（可选）
    # df_a.to_excel(output_path, index=False, header=False)
    #
    # # 查看结果
    # print(df_a.head())


# 使用示例
if __name__ == "__main__":
    # word_c = input("请输入要添加的词C: ")
    file_a_path = r"D:\python\document\A.xlsx"
    file_b_path = r"D:\python\document\B.xlsx"
    output_file = r"D:\python\document\A_processed_pandas.xlsx"

    add_word_c_if_contains_pandas(file_a_path, file_b_path, output_file)