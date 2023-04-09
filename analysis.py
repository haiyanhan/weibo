from aip import AipNlp
import pandas as pd
import numpy as np
import time
import os
# aip库是百度AI开放平台提供的Python SDK，用于调用各种人工智能服务接口，包括自然语言处理、图像识别、语音识别等。
# AipNlp模块是aip库中的一个模块，用于调用百度AI开放平台的   自然语言处理    服务接口，比如文本分类、情感分析、词法分析等。
# pandas是一个数据分析工具，提供了用于处理和分析大量数据的数据结构和函数。它使得数据的清洗、处理、分析和可视化变得更加简单和高效。
# pandas中最常用的数据结构是DataFrame和Series，可以用于读取、处理、过滤、聚合和可视化数据。
# numpy是一个Python科学计算库，提供了高性能的多维数组和矩阵计算功能。它支持向量和矩阵运算、线性代数、傅里叶变换、随机数生成等功能，
# 也提供了许多数学函数和常量。由于numpy的高性能和广泛应用，很多其它科学计算库都以numpy为基础开发。

# 百度大脑 
# 此处输入baiduAIid
APP_ID = '31684453'
API_KEY = 'MYMhj1TuVVDyR4jdUhDKZo5E'
SECRET_KEY = 'irCfV5gRCveK7xrpe6i31mpSzCrLI5Cd'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def isPostive(text):
    try:
        if client.sentimentClassify(text)['items'][0]['positive_prob']>0.5:
            return "积极"
        else:
            return "消极"
    except:
        return "积极"

# 读取文件，注意修改文件路径
# file_path = 'mlxg.xls'
# file_path = 'test.xls'
file_path = 'table.xls'
data = pd.read_excel(file_path,encoding='utf-8')

moods = []
count = 1
for i in data['微博内容']:
    moods.append(isPostive(i))
    count+=1
    print(count)
    # print("目前分析到："+count) 要把count化为str，str（count）

data['情感倾向'] = pd.Series(moods)

# # 此处为覆盖保存
# data.to_excel(file_path)
# print("分析完成，已保存")
# 新建
# new_file_path = 'new_mlxg.xlsx'
new_file_path = 'mlxg.xlsx'
data.to_excel(new_file_path)
print("分析完成，已保存到新文件")

# 在保存到新文件之前判断是否已有文件。上面‘新建’代码是如已有new_mlxg.xlsx则覆盖文件
# new_file_path = 'new_mlxg.xlsx'
# if not os.path.exists(new_file_path):
#     data.to_excel(new_file_path)
#     print("分析完成，已保存到新文件")
# else:
#     print("新文件已经存在，无法保存")

# 读取原始数据
# file_path = 'mlxg.xlsx'
# data = pd.read_excel(file_path)
# 此处为简单分类:P
def fenlei(text):
    xf = ['抽奖',"抽一个","抽一位","买","通贩"]
    cz = ["画","实物","返图","合集","摸鱼","漫","自制","攻略","授权","草稿","绘"]
    gj = ["hz","狗粉丝","狗女儿"]
    for j in cz:
        if j in text:
            return "创作"
    for i in xf:
        if i in text:
            return "消费"
    for k in gj:
        if k in text:
            return "攻击"
    return "其他"
# 对每一行数据进行分类
data['分类'] = data['微博内容'].apply(fenlei)
# data['分类'] = data['微博正文'].apply(fenlei)
# 将带有分类结果的数据保存到Excel文件中
# new_file_path = 'new_mlxg.xlsx'
# new_file_path = 'mlxg.xlsx'
data.to_excel(new_file_path, index=False)
# index=False参数用于禁止保存行索引
print("分类完成，已保存到新文件")

# '''
# # 此处为简单分类:P
# def fenlei(text):
#     xf = ['抽奖',"抽一个","抽一位","买","通贩"]
#     cz = ["画","实物","返图","合集","摸鱼","漫","自制","攻略","授权","草稿","绘"]
#     gj = ["hz","狗粉丝","狗女儿"]
#     for j in cz:
#         if j in text:
#             return "创作"
#     for i in xf:
#         if i in text:
#             return "消费"
#     for k in gj:
#         if k in text:
#             return "攻击"
#     return "其他"        
# ''' 
