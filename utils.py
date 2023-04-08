import time
import pymysql

def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


def get_conn():
    """
    获得数据库连接
    :return:
    """
    conn = pymysql.connect(host="rm-bp1h0j9hp7247tk080o.mysql.rds.aliyuncs.com",
                           user="root",
                           password="iloveCLN12688",
                           db="covid19_public_opinion_system",
                           charset="utf8"
                           )
    cursor = conn.cursor()
        # sql = "select * from hot_search"
        # cursor.execute(sql)
        # res = cursor.fetchall()
        # print(res)
    return conn, cursor


def close_conn(conn, cursor):
    """
    关闭数据库连接
    :param conn:
    :param cursor:
    :return:
    """
    cursor.close()
    conn.close()

def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return:
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


# if __name__ == '__main__':
#     print(get_time())