import pandas as pd


def add_word_c_if_contains_pandas(file_a_path, file_b_path, output_path):

    # 读取B.xls中两个sheet的关键词
    df_related = pd.read_excel(file_b_path, sheet_name='相关', header=None, usecols=[1])
    df_unrelated = pd.read_excel(file_b_path, sheet_name='不相关', header=None, usecols=[1])

    # 提取关键词列表
    related_keywords = df_related[1].dropna().astype(str).tolist()
    unrelated_keywords = df_unrelated[1].dropna().astype(str).tolist()

    # 读取A.xls
    df_a = pd.read_excel(file_a_path, header=None)

    # # 创建布尔掩码，查找related关键词
    # mask_related = df_a[1].apply(lambda x: any(kw in x for kw in related_keywords))
    #
    # # 将匹配的关键词填入第0列（列索引0）
    # def get_first_related_keyword(text):
    #     for kw in related_keywords:
    #         if kw in text:
    #             return kw
    #     return ""
    #
    # df_a.loc[mask_related, 0] = df_a.loc[mask_related, 1].apply(get_first_related_keyword)

    # Pandas 的 str.extract() 和 loc[] 都是 向量化操作，底层使用 NumPy/C 优化，而不是 Python 循环。大数据（如 20 万行）时，向量化方法比循环快 10-100 倍。
    # 不逐行处理：不会像 for 循环或 apply() 那样逐行遍历数据。
    # 批量计算：Pandas 一次性对整个列执行操作（类似 NumPy 的广播机制）。
    #
    # 检查 df_a[1] 是否包含 related_keywords 中的任意一个词
    mask = df_a[1].str.contains('|'.join(related_keywords))

    # 提取第一个匹配的关键词，并填充到第0列
    df_a.loc[mask, 0] = df_a.loc[mask, 1].str.extract(f'({"|".join(related_keywords)})')[0]



    #  ---------------------------------------------------------------
    # 创建布尔掩码，查找unrelated关键词
    mask_unrelated = df_a[1].apply(lambda x: any(kw in x for kw in unrelated_keywords))

    # 把匹配到的长尾词（第1列）迁移到第4列（索引3），然后可以根据需要清空第1列
    df_a.loc[mask_unrelated, 3] = df_a.loc[mask_unrelated, 1]
    df_a.loc[mask_unrelated, 1] = ""  # 删除原来的

    # ----------------------------------------------------------------
    # 保存结果（可选）
    df_a.to_excel(output_path, index=False, header=False)

    # 查看结果
    print(df_a.head())


# 使用示例
if __name__ == "__main__":
    # word_c = input("请输入要添加的词C: ")
    file_a_path = r"D:\python\document\A.xlsx"
    file_b_path = r"D:\python\document\B.xlsx"
    output_file = r"D:\python\document\A_processed_pandas.xlsx"

    add_word_c_if_contains_pandas(file_a_path, file_b_path, output_file)