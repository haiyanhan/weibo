import utils

def queryHotTopicList():
    conn, cursor = utils.get_conn()
    sql = "select topic_name, positive_value, negative_value from hot_topic limit 6"
    data = utils.query(sql)
    utils.close_conn(conn, cursor)
    return data

def querStaGender():
    conn, cursor = utils.get_conn()
    sql = "select male_num, female_num from sta_gender limit 1"
    data = utils.query(sql)
    utils.close_conn(conn, cursor)
    return data

def queryStaProvinceDistribute():
    coon, cursor = utils.get_conn()
    sql = "select stapd_province_name, stapd_sentiment_num from sta_province_distribute"
    data = utils.query(sql)
    utils.close_conn(coon, cursor)
    return data

def queryStaWordFrequency():
    conn, cursor = utils.get_conn()
    sql = "SELECT stawf_word_name, stawf_word_num FROM `sta_word_frequency` ORDER BY stawf_word_num desc"
    data = utils.query(sql)
    utils.close_conn(conn, cursor)
    return data

def queryTopWords():
    conn, cursor = utils.get_conn()
    sql = "SELECT stawf_word_name, stawf_word_num FROM `sta_word_frequency` ORDER BY stawf_word_num desc limit 9"
    data = utils.query(sql)
    utils.close_conn(conn, cursor)
    return data

def queryStaNetizenAttention():
    conn, cursor = utils.get_conn()
    sql = "select attention_num, stana_date from sta_netizen_attention ORDER BY stana_date LIMIT 15"
    data = utils.query(sql)
    utils.close_conn(conn, cursor)
    return data

def queryTopProvinceDistribute():
    conn, cursor = utils.get_conn()
    sql = "select stapd_province_name, stapd_sentiment_num from sta_province_distribute ORDER BY stapd_sentiment_num desc limit 10"
    data = utils.query(sql)
    utils.close_conn(conn, cursor)
    return data