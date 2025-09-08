'''
tdk文本处理成合适的格式
'''
def main():

   # 按双引号分组，每组包含双引号之间的内容
    groups = []
    current_group = []
    in_quotes = False
    
    # 按行处理，识别双引号分组
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        if line.startswith('"') and line.endswith('"'):
            # 单行双引号，直接作为一个组
            clean_line = line.strip('"').strip()
            if clean_line:
                groups.append([clean_line])
        elif line.startswith('"'):
            # 开始双引号，开始新组
            in_quotes = True
            current_group = [line.strip('"').strip()]
        elif line.endswith('"'):
            # 结束双引号，结束当前组
            in_quotes = False
            current_group.append(line.strip('"').strip())
            if current_group:
                groups.append(current_group)
                current_group = []
        elif in_quotes:
            # 在双引号内，添加到当前组
            current_group.append(line.strip())
    
    # 拼接每组内容
    result = []
    for group in groups:
        if group:  # 确保组不为空
            merged = fuhao.join(group)
            result.append(merged)

    # 输出结果
    for r in result:
        print(r)

if __name__ == "__main__":

    fuhao = ","
    text = '''"贵阳银屑病医院一览表
贵阳治疗牛皮癣的医院
贵州治牛皮癣的中医院"
"银屑病365问
头部有牛皮癣如何治疗"
"卡泊三醇对银屑病效果
他克莫司银屑病的效果"
"银屑病308激光治疗有副作用吗
银屑病光疗仪价格"
"牛皮癣会传染人吗
牛皮癣特征"
"头皮寻常型银屑病得病率
儿童会得银屑病关节炎吗"
"银屑病甲能恢复正常吗
治疗银屑病视频"
"兰州银屑病医院怎么样啊
兰州治疗牛皮癣哪家好
甘肃牛皮癣名中医"
"牛皮癣抹什么药最好
牛皮癣使用什么中药"
"银屑病药浴配方
银屑病激光治疗后能用卡泊三醇软膏吗"
"光疗治疗皮肤病有用吗
银屑病308和311哪个效果好"
"牛皮癣好转表现
牛皮癣是什么样子"
"银屑病脸上爆发怎么办
头皮型银屑病怎么得的"
"有人治好过银屑病吗
一般治疗银屑病的价格"
"福州治疗牛皮癣费用
福州银屑病医院怎么样啊
福建治疗银屑病专家"
"牛皮癣老复发怎么办 
牛皮癣药膏不含激素"
"银屑病能用尿素霜吗
消银胶囊治疗银屑病"
"银屑病308激光治疗贵吗
银屑病仪器治疗完为什么发红"
"银屑病能自愈吗
怎么确定是不是银屑病"
"牛皮癣形成的原因
得了银屑病夫妻间会传染么"
"银屑病初期好治愈吗
银屑病头皮上会自愈吗"
"河南银屑病专科医院哪家好
河南省银屑病医院排名
郑州银屑病专病门诊"
"女孩子得了银屑病意味着什么
牛皮癣做光波能好吗"
"银屑病药膏哪个好
银屑病关节炎乌帕替尼还是可善挺"
"光疗的作用与功效
伍德灯可以检查癣吗"
"牛皮癣的临床表现
怎么判断是不是牛皮癣"
"牛皮癣是什么原因造成的
20岁得银屑病正常吗"
"中医能治好银屑病吗
银屑病特效老偏方 "






    '''
    main()
