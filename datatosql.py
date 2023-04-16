import pandas as pd
import MySQLdb
from sqlalchemy import create_engine
# 读取 Excel 文件数据
data = pd.read_excel('table.xls')

# 连接 MySQL 数据库
# conn = MySQLdb.connect(host='localhost',
#                        user='root',
#                        password='123456',
#                        db='topic')
conn = create_engine('mysql+pymysql://root:123456@localhost/topic')
# 连接 MySQL 数据库
engine = create_engine('mysql+pymysql://root:123456@localhost/topic')
conn = engine.connect()
# 将数据写入 MySQL 数据库
data.to_sql(name='weibo_copy', con=conn, if_exists='replace', index=False)

# 关闭数据库连接
conn.close()#weib

#  import pandas as pd
# import pymysql

# # 读取 Excel 文件数据
# data = pd.read_excel('table.xls')

# # 连接 MySQL 数据库
# conn = pymysql.connect(host='localhost',
#                        user='root',
#                        password='123456',
#                        db='topic')

# # 将数据写入 MySQL 数据库
# data.to_sql(name='weibo_copy', con=conn, if_exists='replace', index=False)

# # 关闭数据库连接
# conn.close()

# # 如果在向表格中插入数据时不希望覆盖现有数据，则可以将 if_exists 参数设置为 'append'。这将追加新数据到现有表格的末尾。如果表格不存在，则会创建一个新表格并将新数据添加到其中。