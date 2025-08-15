import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import quote

def search_baidu_and_rank(sentence, target_url):
    """
    在百度中搜索指定句子，并返回目标URL的排名
    
    Args:
        sentence (str): 要搜索的句子
        target_url (str): 目标网站URL
    
    Returns:
        int: 排名（如果找到），否则返回100+
    """
    
    # 百度搜索的基础URL
    base_url = "https://www.baidu.com/s"
    
    # 对搜索词进行URL编码
    encoded_sentence = quote(sentence)
    
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    page_num = 1
    current_rank = 0
    
    while page_num <= 10:  # 最多搜索10页
        try:
            # 构建搜索URL
            if page_num == 1:
                search_url = f"{base_url}?wd={encoded_sentence}"
            else:
                search_url = f"{base_url}?wd={encoded_sentence}&pn={(page_num-1)*10}"
            
            print(f"正在搜索第{page_num}页...")
            
            # 发送请求
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找搜索结果容器
            result_containers = soup.find_all('div', class_='result c-container xpath-log new-pmd')
            
            if not result_containers:
                print(f"第{page_num}页没有找到搜索结果")
                break
            
            # 遍历搜索结果
            for container in result_containers:
                current_rank += 1
                
                # 获取id属性
                container_id = container.get('id', '')
                
                # 检查是否包含目标URL
                if target_url in str(container):
                    print(f"找到目标网站！")
                    print(f"排名: {current_rank}")
                    print(f"容器ID: {container_id}")
                    return current_rank
                
                # 检查id是否大于100（表示排名在100开外）
                if container_id and container_id.isdigit():
                    if int(container_id) > 100:
                        print(f"当前页面容器ID: {container_id} > 100，停止搜索")
                        print(f"目标网站排名: 100+")
                        return "100+"
            
            # 如果当前页面没有找到，继续下一页
            page_num += 1
            
            # 添加延迟，避免被百度封禁
            time.sleep(2)
            
        except requests.RequestException as e:
            print(f"请求第{page_num}页时出错: {e}")
            break
        except Exception as e:
            print(f"处理第{page_num}页时出错: {e}")
            break
    
    # 如果所有页面都搜索完还没找到
    print(f"在所有搜索页面中都没有找到目标网站")
    print(f"目标网站排名: 100+")
    return "100+"

def main():
    """主函数"""
    print("百度搜索结果排名分析工具")
    print("=" * 50)
    
    # 获取用户输入
    target_url = 'fjbbb120.com'
    sentence = '福州博润白斑医院(白癜风诊疗中心)-福州博润治疗白癜风效果怎么样-福州治疗白癜风的专科医院哪家好'
    
    if not target_url or not sentence:
        print("URL和搜索句子不能为空！")
        return
    
    # # 确保URL格式正确
    # if not target_url.startswith(('http://', 'https://')):
    #     target_url = 'https://' + target_url
    
    print(f"\n开始搜索...")
    print(f"目标网站: {target_url}")
    print(f"搜索句子: {sentence}")
    print("-" * 50)
    
    # 执行搜索和排名分析
    rank = search_baidu_and_rank(sentence, target_url)
    
    print("-" * 50)
    print(f"搜索结果: {rank}")

if __name__ == "__main__":
    main()
