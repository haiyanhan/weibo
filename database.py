import pymysql
import datetime

# 创建MySQL连接
conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='topic')
# 判断是否连接成功
# if conn:
#     print("Database connection established successfully")
# else:
#     print("Database connection failed")

# 解析评论数据并存储到MySQL数据库
# def parse_and_save_comments(weibo_id, comments):
#     for comment in comments:
#         comment_id = comment['id']
#         comment_text = comment['text']
#         comment_user_id = comment['user']['id']
#         comment_user_name = comment['user']['screen_name']
#         comment_time = datetime.datetime.strptime(comment['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
#         with conn.cursor() as cursor:
#             sql = "INSERT INTO comments (weibo_id, comment_id, comment_text, comment_user_id, comment_user_name, comment_time) VALUES (%s, %s, %s, %s, %s, %s)"
#             cursor.execute(sql, (weibo_id, comment_id, comment_text, comment_user_id, comment_user_name, comment_time))
#         conn.commit()

# 创建数据库游标对象
# cursor = conn.cursor()
# # 定义插入数据的 SQL 语句
# sql = "INSERT INTO weibo (rid, username, weibo_level, weibo_content, weibo_repost_count, weibo_comment_count, weibo_praise_count, post_time, search_keywords, topic_name, topic_discussion_count, topic_read_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# for item in value1:
#     data = {}
#     # 在这里获取微博数据并赋值给 data 字典
#     # 构造 SQL 语句
#     sql = "INSERT INTO table_name (rid, username, weibo_level, weibo_content, weibo_repost_count, weibo_comment_count, weibo_praise_count, post_time, search_keywords, topic_name, topic_discussion_count, topic_read_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     values = (data["rid"], data["用户名称"], data["微博等级"], data["微博内容"], data["微博转发量"], data["微博评论量"], data["微博点赞"], data["发布时间"], data["搜索关键词"], data["话题名称"], data["话题讨论数"], data["话题阅读数"])
#     # 执行 SQL 语句
#     cursor.execute(sql, values)
#     # 提交事务
# conn.commit()
# cursor.close()
# conn.close()

# 定义要插入的数据
# data = [("1", "user1", 3, "content1", 100, 200, 300, "2022-08-01 01:23:45", "keyword1", "topic1", 50, 200),
#         ("2", "user2", 2, "content2", 50, 100, 150, "2022-08-02 06:23:45", "keyword2", "topic2", 20, 100)]
# 使用 executemany() 方法插入多条数据
# cursor.executemany(sql, data)

# 提交事务
# conn.commit()
# 关闭游标和连接

# # 模拟微博评论数据
# weibo_id = '1234567890'
# comments = [
#     {
#         "id": "1111111111",
#         "text": "评论1",
#         "user": {
#             "id": "111",
#             "screen_name": "user1"
#         },
#         "created_at": "Tue Mar 29 19:44:08 +0800 2022"
#     },
#     {
#         "id": "2222222222",
#         "text": "评论2",
#         "user": {
#             "id": "222",
#             "screen_name": "user2"
#         },
#         "created_at": "Tue Mar 29 19:44:12 +0800 2022"
#     }
# ]

# # 在函数调用前输出微博ID
# print('weibo_id:', weibo_id)  # 输出weibo_id: 1234567890

# # 调用函数，将微博评论数据写入MySQL数据库
# parse_and_save_comments(weibo_id, comments)

# # 关闭数据库连接
# conn.close()

# # 加入微博评论数据
# def insert_comment(weibo_id, comment_id, comment_text, comment_user_id, comment_user_name):
#     with conn.cursor() as cursor:
#         comment_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         sql = "INSERT INTO comments (weibo_id, comment_id, comment_text, comment_user_id, comment_user_name, comment_time) VALUES (%s, %s, %s, %s, %s, %s)"
#         cursor.execute(sql, (weibo_id, comment_id, comment_text, comment_user_id, comment_user_name, comment_time))
#     conn.commit()

# # 查询微博评论数据
# def select_comments(weibo_id):
#     with conn.cursor() as cursor:
#         sql = "SELECT * FROM comments WHERE weibo_id=%s"
#         cursor.execute(sql, (weibo_id,))
#         results = cursor.fetchall()
#         return results

# # 删除微博评论数据
# def delete_comment(weibo_id, comment_id):
#     with conn.cursor() as cursor:
#         sql = "DELETE FROM comments WHERE weibo_id=%s AND comment_id=%s"
#         cursor.execute(sql, (weibo_id, comment_id))
#     conn.commit()