import pymysql
import datetime

# 创建MySQL连接
# conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='topic')

import pandas as pd
import pymysql

# 读取Excel文件数据
data = pd.read_excel('table.xls')

# 连接 MySQL 数据库
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='123456',
                       db='topic')

# 将数据写入 MySQL 数据库
data.to_sql(name='weibo_copy', con=conn, if_exists='replace', index=False)

# 关闭数据库连接
conn.close()