# -*- coding: utf-8 -*-
import jieba
from collections import Counter
import pandas as pd

# 定义了一个保存分词结果的函数 save_seg()，其中参数 filename 表示保存的文件名，参数 cnt 表示 Counter() 对象。
# 函数将结果保存至文件中，文件格式为 词语\t出现次数：统计数量，并且只保存出现次数最多的前 100 个词语。
# 总体来说，这段代码实现了对微博数据的批量分词和词频统计，并将统计结果按文件名存入文件中，以便进行后续的文本分析和处理。
def save_seg(filename,cnt):
    f_out = open(filename,encoding='utf-8',mode='w+')
    result = cnt.most_common(100)
    for ix in result:
        f_out.write(ix[0]+"\t出现次数："+str(ix[1])+"\n")
# 定义要过滤的常用词和常用标点符号。
STOPWORDS = [u'的',u' ',u'\n',u'他', u'地', u'得', u'而', u'了', u'在', u'是', u'我', u'有', u'和', u'就',  u'不', u'人', u'都', u'一', u'一个', u'上', u'也', u'很', u'到', u'说', u'要', u'去', u'你',  u'会', u'着', u'没有', u'看', u'好', u'自己', u'这']
PUNCTUATIONS = [u'。',u'#', u'，', u'“', u'”', u'…', u'？', u'！', u'、', u'；', u'（', u'）']

# 需要进行分词的文件
# wj = ['mlxg','IG+rng','igbanlan','edg','uzi','teamwe','theshy','英雄联盟','jackeylove']
cnt = Counter()
# for file in wj:
wj =['mlxg'];#列表可以有多个文件，mlxg文件
for file in wj:
    data = pd.read_excel(file+'.xlsx',encoding='utf-8') 
    # 如一个文件前面四句可改为下面三
    # filename = 'mlxg.xlsx'
    # cnt = Counter()
    # data = pd.read_excel(filename, encoding='utf-8')
    for l in data['微博内容'].astype(str):
        seg_list = jieba.cut(l)
        # 每个词语的出现次数。
        for seg in seg_list:
            if seg not in STOPWORDS and seg not in PUNCTUATIONS and seg not in wj:
                cnt[seg] = cnt[seg] + 1
    # save_seg("seg_result/"+file+".txt",cnt) # 保存文件 jieba分析语句 先消极积极再分词词频=先analsis再seg
    save_seg(file+".txt",cnt) # 保存文件 jieba分析语句 先消极积极再分词词频=先analsis再seg

# 遍历文件列表 wj 中的所有文件名 file；
# 使用 Pandas 库的 read_excel() 函数读取指定文件名 file 对应的 Excel 文件，并将其转换为 DataFrame 格式的数据 data；
# 针对 data 中的每一行微博内容，使用 jieba 库的 cut() 函数进行分词，并遍历分词结果 seg_list 中的每一个词 seg；
# 判断词语 seg 是否为停用词、标点符号或文件名，如果不是，则将其出现次数加 1；
# 将所有词语的出现次数保存到字典 cnt 中；
# 调用 save_seg() 函数，将统计结果保存到文本文件 "seg_result/"+file+".txt" 中。

# UnicodeEncodeError: 'gbk' codec can't encode character '\U0001f64f' in position 0: illegal multibyte sequence
# 用 write() 函数向文件写入内容时，数据包含了无法编码为 gbk 字符编码的字符、或者使用了无法编译的编码格式
# 使用 open() 函数时指定一个合适的编码集。例如，使用 open(filename,encoding='utf-8') 代替原有的 open(filename)，
# 将打开一个以 utf-8 编码的文件句柄，就可以把所有 unicode 字符以 utf-8 编码写入文件中。
# 将数据使用内置函数 str.encode() 将其转换成指定的编码格式。
# 例如在 write() 函数中使用 str.encode('utf-8') 对字符串进行编码，将其转换为 UTF-8 编码，可以避免出现编码错误的问题。
