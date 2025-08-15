import pandas as pd
import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import quote

# 百度搜索参数
BAIDU_URL = "https://www.baidu.com/s"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}


def get_baidu_rank(query, target_url):
    """
    在百度搜索中查询指定关键词，查找目标URL的排名
    :param query: 搜索关键词
    :param target_url: 目标URL
    :return: 排名 (1-100) 或 "100+" 或 "未找到"
    """
    # 处理关键词中的特殊字符
    encoded_query = quote(query)

    # 最大搜索页数 (每页10条，10页=100条)
    max_page = 10

    for page in range(max_page):
        params = {
            "wd": encoded_query,
            "pn": page * 10  # 百度分页参数 (0=第一页, 10=第二页)
        }

        try:
            # 发送请求
            response = requests.get(BAIDU_URL, params=params, headers=HEADERS, timeout=15)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # 定位搜索结果容器
            content_left = soup.find('div', id='content_left')
            if not content_left:
                print("未找到搜索结果区域")
                continue

            # 获取所有搜索结果
            results = content_left.find_all('div', class_='result c-container')
            if not results:
                print("未找到任何搜索结果")
                continue

            # 遍历当前页的所有结果
            for result in results:
                # 获取结果ID
                result_id = result.get('id', '')

                # 检查ID是否有效
                if result_id.isdigit():
                    rank = int(result_id)
                    # 如果ID超过100则停止搜索
                    if rank > 100:
                        return "100+"

                    mu_url = result['mu']
                    if target_url in mu_url:
                        return result.get('id')

            # 随机延时防止被封
            time.sleep(random.uniform(1.5, 3.5))

        except Exception as e:
            print(f"搜索过程中发生错误: {str(e)}")
            time.sleep(5)

    return "未找到"


# 主程序
def main():
    # 读取Excel文件
    try:
        priority_file_path=r'C:\Users\zhang\Desktop\数据筛选软件\每日任务\查标题在百度中的排名\需要爬.xlsx'
        df = pd.read_excel(priority_file_path, header=None, usecols=[0, 1, 2])
        print(f"成功读取Excel，共{len(df)}行数据")
    except Exception as e:
        print(f"读取Excel文件失败: {str(e)}")
        return

    # 检查列是否存在
    if len(df.columns) < 3:
        print("Excel文件至少需要三列数据")
        return

    # 遍历每一行进行搜索
    for i, row in df.iterrows():
        url = row[1]  # 第二列是URL
        query = row[2]  # 第三列是句子

        print(f"\n正在处理第{i + 1}行: 关键词='{query}'")
        print(f"目标URL: {url}")

        # 获取百度排名
        rank = get_baidu_rank(query, url)
        df.at[i, '排名'] = rank
        print(f"排名结果: {rank}")

        # 每处理5行保存一次进度
        if (i + 1) % 5 == 0:
            df.to_excel(r'C:\Users\zhang\Desktop\数据筛选软件\每日任务\查标题在百度中的排名\需要爬.xlsx', index=False)
            print(f"已保存进度到第{i + 1}行")

    # 保存最终结果
    df.to_excel(r'C:\Users\zhang\Desktop\数据筛选软件\每日任务\查标题在百度中的排名\需要爬.xlsx', index=False)
    print("\n所有数据处理完成！结果已保存到Excel")


if __name__ == "__main__":
    main()