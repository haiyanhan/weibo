import time
import xlrd
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import requests
import json
import excelSave as save
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from database import parse_and_save_comments  # 导入新建的Python文件和函数
import pymysql
import datetime
import pandas as pd

# 用来控制页面滚动
def Transfer_Clicks(browser):
    time.sleep(5)
    try:
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
    except:
        pass
    return "Transfer successfully \n"

#判断页面是否加载出来
def isPresent():
    temp =1
    try: 
        driver.find_elements_by_css_selector('div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
    except:
        temp =0
    return temp

#插入数据
def insert_data(elems,path,name,yuedu,taolun,num,save_pic):
    for elem in elems:
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数       
        rid = rows_old
        #用户名
        weibo_username = elem.find_elements_by_css_selector('h3.m-text-cut')[0].text
        weibo_userlevel = "普通用户"
        #微博等级
        try: 
            weibo_userlevel_color_class = elem.find_elements_by_css_selector("i.m-icon")[0].get_attribute("class").replace("m-icon ","")
            if weibo_userlevel_color_class == "m-icon-yellowv":
                weibo_userlevel = "黄v"
            if weibo_userlevel_color_class == "m-icon-bluev":
                weibo_userlevel = "蓝v"
            if weibo_userlevel_color_class == "m-icon-goldv-static":
                weibo_userlevel = "金v"
            if weibo_userlevel_color_class == "m-icon-club":
                weibo_userlevel = "微博达人"     
        except:
            weibo_userlevel = "普通用户"
        #微博内容
        #点击“全文”，获取完整的微博文字内容
        weibo_content = get_all_text(elem)
        #获取微博图片
        if save_pic:
            num = get_pic(elem,num)
        #获取分享数，评论数和点赞数               
        shares = elem.find_elements_by_css_selector('i.m-font.m-font-forward + h4')[0].text
        if shares == '转发':
            shares = '0'
        comments = elem.find_elements_by_css_selector('i.m-font.m-font-comment + h4')[0].text
        if comments == '评论':
            comments = '0'
        likes = elem.find_elements_by_css_selector('i.m-icon.m-icon-like + h4')[0].text
        if likes == '赞':
            likes = '0'

        #发布时间
        weibo_time = elem.find_elements_by_css_selector('span.time')[0].text
        '''
        print("用户名："+ weibo_username + "|"
              "微博等级："+ weibo_userlevel + "|"
              "微博内容："+ weibo_content + "|"
              "转发："+ shares + "|"
              "评论数："+ comments + "|"
              "点赞数："+ likes + "|"
              "发布时间："+ weibo_time + "|"
              "话题名称" + name + "|" 
              "话题讨论数" + yuedu + "|"
              "话题阅读数" + taolun)
        '''
        value1 = [[rid, weibo_username, weibo_userlevel,weibo_content, shares,comments,likes,weibo_time,keyword,name,yuedu,taolun],]
        # 爬取的数据
        print("当前插入第%d条数据" % rid)
        save.write_excel_xls_append_norepeat(book_name_xls, value1)

# # 读取Excel文件数据
# data = pd.read_excel('book_name_xls.xls')
# # 连接 MySQL 数据库
# conn = pymysql.connect(host='localhost',
#                        user='root',
#                        password='123456',
#                        db='topic')
# # 将数据写入 MySQL 数据库
# data.to_sql(name='weibo', con=conn, if_exists='replace', index=False)
# # 关闭数据库连接
# conn.close()
       
# # 创建MySQL连接
#         conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='topic')
#             # 创建数据库游标对象
#         cursor = conn.cursor()
#         # 定义插入数据的 SQL 语句
#         # sql = "INSERT INTO weibo (rid, weibo_username, weibo_userlevel,weibo_content, shares,comments,likes,weibo_time,keyword,name,yuedu,taolun) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         for item in value1:
#             data = {}
#             # 在这里获取微博数据并赋值给 data 字典
#             # 构造 SQL 语句
#             sql = "INSERT INTO weibo (rid, weibo_username, weibo_userlevel,weibo_content, shares,comments,likes,weibo_time,keyword,name,yuedu,taolun) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#             # values = (data["rid"], data["用户名称"], data["微博等级"], data["微博内容"], data["微博转发量"], data["微博评论量"], data["微博点赞"], data["发布时间"], data["搜索关键词"], data["话题名称"], data["话题讨论数"], data["话题阅读数"])
#             values = [[rid, weibo_username, weibo_userlevel,weibo_content, shares,comments,likes,weibo_time,keyword,name,yuedu,taolun],]           
#             # 执行 SQL 语句
#             cursor.execute(sql, values)
#             # 提交事务
#         conn.commit()
#         cursor.close()
#         conn.close()

#获取“全文”内容
def get_all_text(elem):
    try:
        #判断是否有“全文内容”，若有则将内容存储在weibo_content中
        href = elem.find_element_by_link_text('全文').get_attribute('href')
        driver.execute_script('window.open("{}")'.format(href))
        driver.switch_to.window(driver.window_handles[1])
        weibo_content = driver.find_element_by_class_name('weibo-text').text
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        weibo_content = elem.find_elements_by_css_selector('div.weibo-text')\
                        [0].text
    return weibo_content

def get_pic(elem,num):
    try:
        #获取该条微博中的图片元素,之后遍历每个图片元素，获取图片链接并下载图片
        #如果是多张图片
        if elem.find_elements_by_css_selector\
           ('div > div > article > div > div:nth-child(2) > div > ul > li') != [] :
            pic_links = elem.find_elements_by_css_selector\
           ('div > div > article > div > div:nth-child(2) > div > ul > li')
            for pic_link in pic_links:
                pic_link = pic_link.find_element_by_css_selector\
                           ('div > img').get_attribute('src')
                response = requests.get(pic_link)
                pic = response.content
                with open(pic_addr + str(num) + '.jpg', 'wb') as file:
                    file.write(pic)
                    num += 1
        #如果图片只有一张
        else:
            pic_link = elem.find_element_by_css_selector\
                       ('div > div > article > div > div:nth-child(2) > div > div > img').\
                       get_attribute('src')
            response = requests.get(pic_link)
            pic = response.content
            with open(pic_addr + str(num) + '.jpg', 'wb') as file:
                file.write(pic)
                num += 1
    except Exception as e:
        print(e)
    return num
    
#获取当前页面的数据
def get_current_weibo_data(elems,book_name_xls,name,yuedu,taolun,maxWeibo,num):
    #开始爬取数据
        before = 0 
        after = 0
        n = 0 
        timeToSleep = 100
        while True:
            before = after
            Transfer_Clicks(driver)
            time.sleep(3)
            elems = driver.find_elements_by_css_selector('div.card.m-panel.card9')
            print("当前包含微博最大数量：%d,n当前的值为：%d, n值到5说明已无法解析出新的微博" % (len(elems),n))
            after = len(elems)
            if after > before:
                n = 0
            if after == before:        
                n = n + 1
            if n == 5:
                print("当前关键词最大微博数为：%d" % after)
                insert_data(elems,book_name_xls,name,yuedu,taolun,num,save_pic)
                break
            if len(elems)>maxWeibo:
                print("当前微博数以达到%d条"%maxWeibo)
                insert_data(elems,book_name_xls,name,yuedu,taolun,num,save_pic)
                break
            '''
            if after > timeToSleep:
                print("抓取到%d多条，插入当前新抓取数据并休眠5秒" % timeToSleep)
                timeToSleep = timeToSleep + 100
                insert_data(elems,book_name_xls,name,yuedu,taolun,num,save_pic) 
                time.sleep(5) 
            '''
#爬虫运行 
def spider(username,password,book_name_xls,sheet_name_xls,keyword,maxWeibo,num,save_pic):
    
    #创建文件
    if os.path.exists(book_name_xls):
        print("文件已存在")
    else:
        print("文件不存在，重新创建")
        # weibo_id
        value_title = [["rid", "用户名称", "微博等级", "微博内容", "微博转发量","微博评论量","微博点赞","发布时间","搜索关键词","话题名称","话题讨论数","话题阅读数"],]
        #? value_title = [["rid", "name", "grade", "text", "zhuanfa","comment","dianzan","time","keyword","theme","taolun","yuedu"],]
        save.write_excel_xls(book_name_xls, sheet_name_xls, value_title)

    # 写入数据库
    
    #加载驱动，使用浏览器打开指定网址  
    driver.set_window_size(452, 790)
    driver.get('https://m.weibo.cn')
    
    driver.get("https://passport.weibo.cn/signin/login")
    print("开始自动登陆，若出现验证码手动验证")
    time.sleep(3)

    elem = driver.find_element_by_xpath("//*[@id='loginName']");
    elem.send_keys(username)
    elem = driver.find_element_by_xpath("//*[@id='loginPassword']");
    elem.send_keys(password)
    elem = driver.find_element_by_xpath("//*[@id='loginAction']");
    elem.send_keys(Keys.ENTER)  
    print("暂停20秒，用于验证码验证")
    time.sleep(2)    
    
    # 添加cookie
    #将提前从chrome控制台中复制来的cookie保存在txt中，转化成name, value形式传给的driver
    #实现自动登录
    #如果txt中的cookie是用保存的，则可以直接使用, 无需转化
    '''
    driver.delete_all_cookies()
    with open(r'./weibocookie.txt') as file:
        cookies = json.loads(file.read())
    for name, value in cookies.items():
        print(name, value)
        driver.add_cookie({'name': name, 'value': value})
    driver.refresh()
    '''
       
    while 1:  # 循环条件为1必定成立
        result = isPresent()
        # 解决输入验证码无法跳转的问题
        driver.get('https://m.weibo.cn/') 
        print ('判断页面1成功 0失败  结果是=%d' % result )
        if result == 1:
            elems = driver.find_elements_by_css_selector('div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
            #return elems #如果封装函数，返回页面
            break
        else:
            print ('页面还没加载出来呢')
            time.sleep(20)
    time.sleep(2)

    #搜索关键词 //*[@id="app"]/div[1]/div[1]/div[1]/div/div/div[2]/form/input
    elem = driver.find_element_by_xpath("//*[@class='m-text-cut']").click();
    # 改元素=微博话题的名称     点击搜索框
    time.sleep(2)
    # elem = driver.find_element_by_xpath("//*[@type='search']");
    # 定位搜索栏
    elem = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[1]/div/div/div[2]/form/input");
    # //*[@id="app"]/div[1]/div[1]/div[1]/div/div/div[2]/form/input
    
    # 点击搜索按钮
    elem.send_keys(keyword)
    elem.send_keys(Keys.ENTER)
    time.sleep(5)

#   删去了下面的，搜索关键词带##直接跳转到疫情超话界面
    # elem = driver.find_element_by_xpath("//*[@class='box-left m-box-col m-box-center-a']") 
    # 修改为点击超话图标进入超话，减少错误    
    # 搜索疫情--点击话题--点击#疫情#（讨论，阅读）--点击超话疫情（帖子粉丝）--
    # elem = driver.find_element_by_xpath("//img[@src ='http://simg.s.weibo.com/20181009184948_super_topic_bg_small.png']")
    # elem=driver.find_element_by_css_selector("#app > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div.module-page-fragment > div.m-container-max.m-top-nav > div > div > div > ul > li:nth-child(10) > span")
    
#     elem = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/li[10]/span")
# #    搜索肺炎后，点击搜索框下的超话按钮，
# # 然后进入第一个肺炎超话。  直接搜索#疫情#进入超话
#     elem.click()
    print("超话链接获取完毕，休眠2秒")
    time.sleep(2)  

# 据gpt
    # # 等待元素加载完成，超时时间为 5 秒
    # elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "super-topic")]/a')))  
    # # 在获取 yuedu_taolun 前先等待 1 秒
    # time.sleep(1)
    # yuedu_taolun = elem.text
    # # 在获取 yuedu 和 taolun 前分别等待 1 秒和 2 秒
    # time.sleep(1)
    # yuedu = driver.find_element_by_xpath('//span[contains(text(),"阅读")]/following-sibling::span').text
    # time.sleep(2)
    # taolun = driver.find_element_by_xpath('//span[contains(text(),"讨论")]/following-sibling::span').text
# 把阅读讨论数的xpath复制下来定位到阅读讨论数元素
    # # 等待元素加载完成，超时时间为 5 秒
    # elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div/div/div[2]/h4[2]/span')))  
    # # 在获取 yuedu_taolun 前先等待 1 秒
    # time.sleep(1)
    # yuedu_taolun = elem.text
    # # 在获取 yuedu 和 taolun 前分别等待 1 秒和 2 秒
    # time.sleep(1)
    # yuedu = driver.find_element_by_xpath('//span[contains(text(),"阅读")]/following-sibling::span').text
    # time.sleep(2)
    # taolun = driver.find_element_by_xpath('//span[contains(text(),"讨论")]/following-sibling::span').text
# gpt
    # # 获取每个卡片的信息
    # cards = driver.find_elements_by_xpath('//div[@class="card m-panel card4"]')
    # # 遍历每个卡片
    # for card in cards:
    # # 获取超话名称
    #     element = card.find_element_by_xpath('.//div[contains(@class, "super-topic")]/a')
    #     chao_hua = element.text   
    #     # 获取阅读量和讨论量
    #     element_text = card.text
    #     yuedu = re.search(r'\d+', element_text).group()
    #     taolun = re.search(r'\d+', element_text.split('讨论')[1]).group()  
    #     # 输出卡片信息
    #     print("超话名称：", chao_hua)
    #     print("阅读量：", yuedu)
    #     print("讨论量：", taolun)
# 原文档 translate是过滤函数，split是分隔
# 通过 xpath 定位元素
    # yuedu_taolun = driver.find_element_by_xpath("//span[@class='card-title']")
    # 报错 Unable to locate element: {"method":"xpath","selector":"//span[@class='card-title']"}
    # yuedu_taolun = driver.find_element_by_css_selector("'app'>'div':nth-child(1) > div:nth-child(1) > div.npage-bg.no-bg > div > div > div.m-box-col.m-box-dir.npg-desc > h4:nth-child(2) > span")
#    报错selenium.common.exceptions.InvalidSelectorException: Message: invalid selector: An invalid or illegal selector was specified
    # yuedu_taolun = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[1]/div[4]/div/div/div/a/div[2]/h4[1]").text
    yuedu_taolun = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[2]/div/div/div[2]/h4[2]/span").text
    # print("过滤前: yuedu_taolun =", yuedu_taolun)
    # yuedu_taolun = yuedu_taolun.translate(str.maketrans("", "", "\t\n\x0b\x0c\r\xa0\u3000\x9a")).strip()
    # print("过滤后: yuedu_taolun =", yuedu_taolun)
    # yuedu = yuedu_taolun.split("　")[0]
    # taolun = yuedu_taolun.split("　")[1]
    yuedu = yuedu_taolun.split(" ")[0]
    taolun = yuedu_taolun.split(" ")[1]
    # taolun = yuedu_taolun.split("  ")[1] 是全角空格！=中文的空格，要设置为全角
    # #上面两句合二为一      yuedu, taolun = yuedu_taolun.split("　　")

# str.maketrans("", "", "\t\n\x0b\x0c\r\xa0\u3000\x9a") 中的第一个空字符串表示将不需要替换的字符映射为它本身，
# 第二个空字符串表示将需要替换的字符映射为空字符串，即删除。
# 将字符串中的制表符、换行符、回车符、不间断空格、全角空格和其他一些特殊字符删除。

    #打印错误信息
    #print("Error: yuedu_taolun =", yuedu_taolun)
    # 过滤掉非数字（\D）和非全角空格字符    - 7266 20 -
    # yuedu_taolun = yuedu_taolun.translate(str.maketrans("", "", "\t\n\x0b\x0c\r\xa0\u3000\x9a")).strip()
    # 检查拆分出的子字符串数量是否符合预期
    # parts = yuedu_taolun.split("　")
    # #即使报错程序也不奔溃
    # if len(parts) == 2:
    #     yuedu, taolun = parts
    # else:
    #     # 处理异常或错误情况，例如输出日志或者抛出异常
    #     print("字符串格式错误", yuedu_taolun)

    time.sleep(2)
    name = keyword   
    #  //*[@id="app"]/div[1]/div[1]/div[1]/div[4]/div/div/div/a/div[2]/h4[1] 超话里帖子那行
    # shishi_element = driver.find_element_by_xpath("//*[@class='scroll-box nav_item']/ul/li/span[text()='帖子']")
    # shishi_element = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div/div[3]/div/div/h4")
    # shishi_element = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div")
    get_current_weibo_data(elems,book_name_xls,name,yuedu,taolun,maxWeibo,num) #爬取实时
    time.sleep(2)
  
if __name__ == '__main__':
    username = "你的微博登录名" #你的微博登录名
    password = "你的微博登录名" #你的密码   
    # driver.get('https://m.weibo.cn')
    # driver_path ="C:\\Users\han\.cache\selenium\chromedriver\win32\111.0.5563.64"
    driver_path ="./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path )
    #你的chromedriver的地址
    driver.implicitly_wait(2)#隐式等待2秒

    # book_name_xls = "test.xls" #填写你想存放excel的路径，没有文件会自动创建 mlxg
    book_name_xls = "table.xls" 

#？ # 读取Excel文件数据
    # data = pd.read_excel('table.xls')
    # # 连接 MySQL 数据库
    # conn = pymysql.connect(host='localhost',
    #                     user='root',
    #                     password='123456',
    #                     db='topic')
    # # 将数据写入 MySQL 数据库
    # data.to_sql(name='weibo', con=conn, if_exists='replace', index=False)
    # # 关闭数据库连接
    # conn.close()

    sheet_name_xls = '微博数据' #sheet表名 数据写入xls的微博数据列
    maxWeibo = 10 #设置最多多少条微博
    keywords = ["#疫情#",] # 此处可以设置多个超话关键词
    num = 1
    save_pic = False  #设置是否同时爬取微博图片，默认不爬取
    pic_addr = 'img/' #设置自己想要放置图片的路径
    
    # 将解析的评论数据写入MySQL数据库
    # parse_and_save_comments(weibo_id, comments)

# def parse_weibo_page(weibo_id, page):
#     url = f"https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0&page={page}"
#     headers = {
#         "User-Agent": UserAgent().random,
#         "Referer": f"https://m.weibo.cn/detail/{weibo_id}",
#         "X-Requested-With": "XMLHttpRequest",
#     }
#     response = s.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         if data.get("ok") == 1:
#             comments = data.get("data").get("data")
#             if comments:
#                 # 在这里调用新建的Python文件中的`parse_and_save_comments`函数
#                 parse_and_save_comments(weibo_id, comments)
#                 return True
#     return False

    for keyword in keywords:
        spider(username,password,book_name_xls,sheet_name_xls,keyword,maxWeibo,num,save_pic)
driver.quit() 
# 关闭网页
