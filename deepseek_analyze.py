import json
import time
import pandas as pd
from openai import OpenAI
from typing import List, Dict, Any


def analyze_sentences(sentences: List[str], api_key: str, batch_size: int = 20) -> List[Dict[str, Any]]:
    """
    使用DeepSeek API分析句子与白癜风和银屑病的相关性

    Args:
        sentences: 句子列表
        api_key: DeepSeek API密钥
        batch_size: 每批处理的句子数量

    Returns:
        分析结果列表
    """
    client = OpenAI(
        api_key="sk-422aa260c2724c9cb8fce5e60e17b924",
        base_url="https://api.deepseek.com"
    )

    results = []

    # 分批处理句子以减少API调用次数
    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i + batch_size]
        print(f"处理批次 {i // batch_size + 1}/{(len(sentences) - 1) // batch_size + 1}")

        # 构建批量处理的提示
        prompt = build_batch_prompt(batch)

        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的医学数据分析助手，擅长分析皮肤病相关文本。"},
                    {"role": "user", "content": prompt}
                ],
                stream=False,
                temperature=0.1  # 低温度以获得更确定的输出
            )

            # 解析响应
            batch_results = parse_response(response.choices[0].message.content, batch)
            results.extend(batch_results)

            # 添加延迟以避免API限制
            time.sleep(1)

        except Exception as e:
            print(f"处理批次时出错: {e}")
            # 如果出错，为这批句子添加默认结果
            for sentence in batch:
                results.append({
                    "sentence": sentence,
                    "score": 0.0,
                    "keywords": [],
                    "error": str(e)
                })

    return results


def build_batch_prompt(sentences: List[str]) -> str:
    """
    构建批量处理的提示

    Args:
        sentences: 句子列表

    Returns:
        提示文本
    """
    sentences_text = "\n".join([f"{i + 1}. {s}" for i, s in enumerate(sentences)])

    return f"""请分析以下句子与白癜风和银屑病的相关性，并按照要求输出JSON格式的结果。

要求：
1. 分析每个句子与白癜风和银屑病的相关性，给出0-1之间的分数（精确到0.01）,
2. 如果分数大于0.5，提取句子中的关键词（即使有拼写错误也要识别，纠正后输出，比如白点巅峰，正确的应该是 白癜风,）
3. 输出格式为JSON列表，每个元素包含：score(分数), keywords(关键词列表), sentence(原句子)

句子列表：
{sentences_text}

请直接输出JSON格式的结果，不要添加任何其他内容。"""


def parse_response(response_text: str, original_sentences: List[str]) -> List[Dict[str, Any]]:
    """
    解析API响应

    Args:
        response_text: API响应文本
        original_sentences: 原始句子列表（用于验证）

    Returns:
        解析后的结果列表
    """
    try:
        # 尝试从响应中提取JSON
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1

        if start_idx == -1 or end_idx == 0:
            raise ValueError("响应中未找到JSON数组")

        json_str = response_text[start_idx:end_idx]
        results = json.loads(json_str)

        # 验证结果数量与输入句子数量一致
        if len(results) != len(original_sentences):
            raise ValueError(f"结果数量({len(results)})与输入句子数量({len(original_sentences)})不匹配")

        # 确保每个结果都包含必要的字段
        for i, result in enumerate(results):
            if "sentence" not in result:
                result["sentence"] = original_sentences[i]
            if "score" not in result:
                result["score"] = 0.0
            if "keywords" not in result:
                result["keywords"] = []

        return results

    except Exception as e:
        print(f"解析响应时出错: {e}")
        print(f"响应内容: {response_text}")

        # 如果解析失败，创建默认结果
        default_results = []
        for sentence in original_sentences:
            default_results.append({
                "sentence": sentence,
                "score": 0.0,
                "keywords": [],
                "error": str(e)
            })

        return default_results


def save_to_excel(results: List[Dict[str, Any]], filename: str):
    """
    将结果保存到Excel文件

    Args:
        results: 分析结果列表
        filename: 输出文件名
    """
    # 转换为DataFrame
    df = pd.DataFrame(results)

    # 重新排列列的顺序
    if "error" in df.columns:
        df = df[["sentence", "score", "keywords", "error"]]
    else:
        df = df[["sentence", "score", "keywords"]]

    # 保存到Excel
    df.to_excel(filename, index=False)
    print(f"结果已保存到 {filename}")


def main():
    # 这里是你的句子列表，示例数据
    sentences = [
        "孩子身上有白色的胎记是什么情况引起的",
        "婴儿眼尾皮肤白是什么原因导致的",
        "阿昔替尼的作用",
        "孩子脸上一大块白的",
        "白点癫风怎么治",
        "白点巅峰怎么治",
        "白点风"
        # 这里可以添加更多句子，最多约1w句
    ]

    # 你的DeepSeek API密钥
    api_key = "你的DeepSeek_API密钥"  # 请替换为你的实际API密钥

    # 分析句子
    print("开始分析句子...")
    results = analyze_sentences(sentences, api_key, batch_size=20)  # 较小的批次大小以提高成功率

    # 保存结果到Excel
    save_to_excel(results, "D:\sort\deepseek分析.xlsx")
    print("分析完成!")


if __name__ == "__main__":
    main()