import pandas as pd


def add_word_c_if_contains_pandas(input_word_c, file_a_path, file_b_path, output_path):
    # 读取B.xls的关键词（假设B列是第2列）
    # df_b = pd.read_excel(file_b_path, header=None, usecols=[1])  # 读取B列
    df_b = pd.read_excel(file_b, sheet_name='related', header=None, usecols=[1])
    keywords = df_b[1].dropna().astype(str).tolist()  # 转为字符串列表

    # 读取A.xls的长词（假设B列是第2列）
    df_a = pd.read_excel(file_a_path, header=None)

    # 检查A的B列是否包含B的任意关键词
    mask = df_a[1].astype(str).apply(
        lambda x: any(keyword in x for keyword in keywords)
    )


    # 在A的A列符合条件的行填入词
    print(df_a.columns)
    # 输出Index([0, 1], dtype='int64')，下面填入0列
    # 你需要在赋值前，手动将目标列转换为字符串类型，以消除警告并避免未来错误：
    # df_a[0] = df_a[0].astype(str)
    df_a.loc[mask, 0] = input_word_c



    # 保存结果（保持原格式）
    df_a.to_excel(output_path, index=False, header=False)
    print(f"处理完成，结果已保存到: {output_path}")


# 使用示例
if __name__ == "__main__":
    word_c = input("请输入要添加的词C: ")
    file_a = r"D:\python\document\A.xlsx"
    file_b = r"D:\python\document\B.xlsx"
    output_file = r"D:\python\document\A_processed_pandas.xlsx"

    add_word_c_if_contains_pandas(word_c, file_a, file_b, output_file)