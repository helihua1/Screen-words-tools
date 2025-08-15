import pandas as pd


# 读取B.xls中两个sheet的关键词
def read_keywords(file_path):
    df_related = pd.read_excel(file_path, sheet_name='相关', header=None, usecols=[1])
    df_unrelated = pd.read_excel(file_path, sheet_name='不相关', header=None, usecols=[1])
    return (
        df_related[1].dropna().astype(str).tolist(),
        df_unrelated[1].dropna().astype(str).tolist()
    )


# 读取sheetX的词对
def read_word_pairs(file_path):
    # 获取所有sheet名
    sheets = pd.ExcelFile(file_path).sheet_names
    # 排除前两个sheet
    word_pairs = []
    for sheet in sheets[2:]:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None, usecols=[0, 1])
        word_pairs.extend(df.values.tolist())
    return word_pairs


# 主处理函数
def process_files(file_a_path, file_b_path):
    # 读取关键词
    related_keywords, unrelated_keywords = read_keywords(file_b_path)

    # 读取词对
    word_pairs = read_word_pairs(file_b_path)

    # 读取A表数据
    df_a = pd.read_excel(file_a_path, header=None)

    # 确保有足够的列
    if len(df_a.columns) < 6:
        for i in range(len(df_a.columns), 6):
            df_a[i] = ""

    # 创建布尔掩码
    mask_related = df_a[1].astype(str).apply(
        lambda x: any(kw in x for kw in related_keywords)
    )

    # 处理匹配到的行
    for idx in df_a[mask_related].index:
        text = str(df_a.at[idx, 1])

        # 检查是否满足词对条件
        moved = False
        for word1, word2 in word_pairs:
            word1, word2 = str(word1), str(word2)
            if word1 in text and word2 in text and text.find(word1) < text.find(word2):
                # 移动到第6列
                df_a.at[idx, 5] = text
                # 清空原位置
                df_a.at[idx, 1] = ""
                moved = True
                break

        if not moved:
            # 添加related关键词到前面
            for kw in related_keywords:
                if kw in text:
                    df_a.at[idx, 0] = kw
                    break

    return df_a


if __name__ == "__main__":
    # word_c = input("请输入要添加的词C: ")
    file_a_path = r"D:\python\document\A.xlsx"
    file_b_path = r"D:\python\document\B.xlsx"
    output_file = r"D:\python\document\A_processed_pandas.xlsx"
result_df = process_files(file_a_path, file_b_path)

# 保存结果
result_df.to_excel("结果.xlsx", index=False, header=False)