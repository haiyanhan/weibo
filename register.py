import json
import secrets
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_login import logout_user
import pymysql
from flask import send_from_directory
from flask_cors import CORS
import requests
from flask import Blueprint
from flask import redirect
from flask import flash, url_for
from flask_login import login_required, current_user
# from register import app
# from register import db
import hashlib
import utils
import getDatas
from flask_login import LoginManager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask import make_response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

# 改密
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length, EqualTo

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'topic'
mysql = MySQL(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/topic'
db = SQLAlchemy(app)

# 区分大小写，且users位置也区分
users = []

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     删除可以登录，要重启才删除，删除浏览器cokkie但没用
# 删除成功后随便在py文件敲几下重新加载了数据库，maybe清除cookie后要重新获取MySQL数据

# ChangePasswordForm新版本要设置为返回bool


class ChangePasswordForm(FlaskForm):
    password = PasswordField('当前密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[
                                 DataRequired(), EqualTo('repassword', message='新密码和确认密码不一致')])
    repassword = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('改密码')

    def validate_on_submit(self) -> bool:
        return super().validate() and self.submit.data


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = password  # generate_password_hash(password)

    def check_password(self, password):
        print("@@@", self.password, password)
        return self.password == password
        # return check_password_hash(self.password, password)
# 添加密码哈希方法
# def set_password(self, password):
#     self.password_hash = generate_password_hash(password)
# # 添加密码校验方法
# def check_password(self, password):
#     return check_password_hash(self.password_hash, password)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    # 获取当前登录用户的用户名
    username = session.get('username')
    print("11111111111", username)
    if not username:
        # 如果没有登录，则重定向到登录页面
        return redirect(url_for('login'))
    # 验证登录成功了
    form = ChangePasswordForm()
    print("222222", form)
    if form.validate_on_submit():
        # 查询用户名为当前登录用户的记录
        user = Users.query.filter_by(username=username).first()
        print(user)
        # 检查输入的当前密码是否正确
        if not user.check_password(form.password.data):
            flash('当前密码不正确，请重新输入')
            return redirect(url_for('change_password'))
        # 检查新密码和确认密码是否一致
        # if form.password.data != form.repassword.data:
        print("2222", form.new_password.data, form.repassword.data)
        if form.new_password.data != form.repassword.data:
            flash('新密码和确认密码不一致，请重新输入')
            print(2222222222222)
            return redirect(url_for('change_password'))
        # 更新用户密码
        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash('密码修改成功')
        return redirect(url_for('index'))
    return render_template('change_password.html', form=form)

# 删除用户


@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    # 获取当前登录用户的用户名
    username = session.get('username')
    if not username:
        # 如果没有登录，则重定向到登录页面
        return redirect(url_for('login'))
    # 查询用户名为当前登录用户的记录
    user = Users.query.filter_by(username=username).first()
    # 删除用户记录
    db.session.delete(user)
    db.session.commit()
    # 清除用户登录状态
    session.pop('username', None)
    session.pop('logged_in', None)
    # 创建一个响应对象，设置 Set-Cookie 响应头，将 cookie 的过期时间设置为一个过去的时间点
    response = make_response(redirect(url_for('index')))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('logged_in', '', expires=0)
    # 返回删除成功信息
    flash('删除成功')
    # 重定向到首页
    return response


# !
# @app.route('/delete_account')
# 跳转不到删除页
# @app.route('/delete_account', methods=['POST'])
# @login_required
# def delete_account():
#     # Delete the user from the database
#     db.session.delete(current_user)
#     db.session.commit()
#     flash('Your account has been deleted', 'success')
#     # Redirect to the index page or any other page you choose
#     return redirect(url_for('index'))
# 点击删除页按钮 删除不了
# def delete_account():
#     if request.method == 'POST':
#         # 获取要删除的用户id
#         user_id = int(request.form.get('user_id'))
#         # 从users列表中找到对应的用户信息
#         user = next((u for u in users if u['id'] == user_id), None)
#         if user:
#             # 如果找到了对应的用户信息，则将该用户从users列表中删除
#             users.remove(user)
#             return redirect(url_for('index'))
#     return render_template('delete_account.html', users=users)
# @app.route('/')
# def index():
#     return render_template('index.html', users=users)

# def delete_account():
#     if request.method == 'POST':
#         # 获取要删除的用户id
#         user_id = int(request.form.get('user_id'))
#         # 从users列表中找到对应的用户信息
#         user = next((u for u in users if u['id'] == user_id), None)
#         if user:
#             # 如果找到了对应的用户信息，则将该用户从users列表中删除
#             users.remove(user)
#             return redirect(url_for('index'))
#     return render_template('delete_account.html', users=users)

# 删除可以登录，要重启才删除
# def delete_account():
#     # 获取当前登录用户的用户名
#     username = session.get('username')
#     if not username:
#         # 如果没有登录，则重定向到登录页面
#         return redirect(url_for('login'))
#     # 查询用户名为当前登录用户的记录
#     user = Users.query.filter_by(username=username).first()
#     # if not user:
#     #     # 如果用户不存在，则返回错误信息
#     #     flash('User does not exist')
#     #     print('User does not exist')
#     #     return redirect(url_for('index'))
#     # 删除用户记录
#     db.session.delete(user)
#     db.session.commit()
#     # 清除用户登录状态
#     session.pop('username', None)
#     # 返回删除成功信息
#     flash('Your account has been deleted')
#     # 清除用户登录状态
#     session.pop('logged_in', None)
#     # 返回删除成功信息
#     flash('Your login has been deleted')
#     # 重定向到首页
#     return redirect(url_for('index'))
 # 如果用户还没有提交确认表单，则渲染确认页面
# return render_template('delete_account.html')

# login_manager = LoginManager()
# login_manager.init_app(app)
# from flask_login import UserMixin
# class User(UserMixin):
#     pass
# @login_manager.user_loader
# def load_user(user_id):
#     # 根据用户 ID 加载用户对象
#     return User.get(user_id)
# from flask_login import LoginManager, UserMixin, AnonymousUserMixin
# class User(UserMixin):
#     pass
# class Anonymous(AnonymousUserMixin):
#     pass
# @login_manager.request_loader
# def load_user_from_request(request):
#     # 从请求中获取用户凭据
#     api_key = request.args.get('api_key')
#     if api_key:
#         # 根据凭据加载用户对象
#         user = User.get(api_key)
#         if user:
#             return user
#     # 如果凭据无效，则返回匿名用户
#     return Anonymous()
# from flask_login import LoginManager, UserMixin, AnonymousUserMixin
# from yourapp import app, db
# from yourapp.models import User
# class Anonymous(AnonymousUserMixin):
#     def __init__(self):
#         self.id = None
#         self.name = 'Guest'
#         self.is_authenticated = False
#         self.is_active = False
#         self.is_anonymous = True
# @login_manager.request_loader
# def load_user_from_request(request):
#     api_key = request.headers.get('Authorization')
#     if api_key:
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user
#     return Anonymous()
# # 改密
# @app.route('/change_password', methods=['GET', 'POST'])
# @login_required
# # 只有登录才显示的视图
# def change_password():
#     if request.method == 'POST':
#         current_password = request.form['current_password']
#         new_password = request.form['new_password']
#         confirm_new_password = request.form['confirm_new_password']
#         if hashlib.sha256(current_password.encode('utf-8')).hexdigest() == current_user.password:
#             if new_password != confirm_new_password:
#                 flash('两次密码不一致.')
#             else:
#                 current_user.password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
#                 cursor = mysql.connection.cursor()
#                 cursor.execute('SELECT * FROM users where password='+current_password)
#                 rows = cursor.fetchall()
#                 cursor = mysql.connection.cursor()
#                 cursor.session.commit()
#                 # db.session.commit()
#                 flash('密码已修改成功.')
#                 return redirect(url_for('index'))
#         else:
#             flash('原密码不正确.')
#     return render_template('change_password.html')


# 钩子函数，每次打开第一件做的事情
@app.before_first_request
def load_users():
    users = Users.query.all()
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM users')
    # rows = cursor.fetchall()
    # # users = []
    # for row in rows:
    #     user = {'id': row[0], 'username': row[1], 'password': row[2]}
    #     users.append(user)
    # cursor.close()
    app.config['USERS'] = users
    # register.py['users'] = users


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# 字典
# users = [{'username': 'admin', 'password': 'asd123'}]  # https://blog.csdn.net/weixin_36380516/article/details/80008602


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':                       # 为什么要写这个if判断是否POST方式。如果不加的话可能报错......因为网页跳转也在这个路由上实现
        username = request.form.get("username")       # POST方式
        password = request.form.get("password")
        repassword = request.form.get('repassword')

        # 判断有无重名
        # 查询用户名为当前登录用户的记录
        user = Users.query.filter_by(username=username).first()
        if user:
            return '用户名已被注册'
        # # 清除用户登录状态
        # for i in users:
        #     if i['username'] == username:
        #         return '用户名已被注册'
        # 判断俩次密码是否一致
        if password == repassword and password != '' and username != '':
            # user = {'username': username, 'password': password}
            # # 写入show
            # users.append(user)
            # # 下面三句是把信息写入数据库
            # cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            # mysql.connection.commit()
            # cursor.close()
            user = Users()
            user.username = username
            user.password = password
            db.session.add(user)
            db.session.commit()
            flash("注册成功")
            return redirect(url_for('login'))
        return "俩次密码不一致，或未输入密码"
    return render_template('register.html')

# @app.route('/search')
# def search():
#     for i in users:
#         if i['username'] == 'aa':
#             return '用户名已被注册'
#         return "未注册"

# @app.route('/weiboindex.html')
# def weiboindex():
#     print(conn)
#     # 从数据库中读取数据
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM weibo')
#     data = cursor.fetchall()
#     # print(data)
#     # #  获取查询结果
#     cursor.close()
#     # # 将数据传递给前台模板
#     # return data[0]
#     return render_template('weiboindex.html', data=data)


@app.route('/function')
def function():
    return render_template('function.html')


@app.route('/houtai')
def houtai():
    return render_template('houtai.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        l_username = request.form.get("l_username")
        l_password = request.form.get("l_password")
        user = Users.query.filter_by(username=l_username).first()
        if user:
            # if i.username != l_username:
            #     return "用户名未注册"
            if user.username == l_username and l_username == 'admin' and user.password == l_password:
                # return "登录成功管理员页面"
                print("admin")
                return redirect('/houtai')
                # return redirect('/admin')
            elif user.username == l_username and user.password == l_password:
                # return "登录成功用户页面"
                print("login")
                # ？登录成功获取l_username
                session['username'] = l_username
                print(session.get('username'))
                return redirect('/function')
                # return redirect('/data')

                # return render_template('weiboindex.html', data=data)
                # return render_template('http://127.0.0.1:5000 ')  #TemplateNotFound
            if user.username == l_username and user.password != l_password:
                return "密码输入错误"
            # print(i, len(users))
        return "用户名未注册"
    return render_template('login.html')


conn = pymysql.connect(host='localhost', user='root', password='123456', database='topic', charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
# 检查连接是否成功
if conn:
    print('数据库连接成功！')
else:
    print('数据库连接失败！')


@app.route('/data')
def data():
    print(conn)
    # 从数据库中读取数据
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weibo')
    data = cursor.fetchall()
    # print(data)
    # #  获取查询结果
    cursor.close()
    # # 将数据传递给前台模板
    # return data[0]
    # 获取查询字符串中的page参数的值，默认为1
    page = int(request.args.get('page', 1))
    # 计算分页所需的参数
    per_page = 4
    total_pages = (len(data) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    # total_pages = (len(data) + per_page - 1+4) // per_page
    # start = (page - 1) * per_page+1
    # end = start + per_page+1
    # total_pages = (len(data)/4) // per_page
    # start = 1
    # end =  (len(data)/4)
    # 对数据进行分页处理
    data = data[start:end]
    return render_template('weiboindex.html', data=data, total_pages=total_pages, page=page)

# 不需要app2，直接写在这


@app.route('/admin')
def admin():
    print(conn)
    # 从数据库中读取数据
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weibo')
    data = cursor.fetchall()
    # print(data)
    # #  获取查询结果
    cursor.close()
    # # 将数据传递给前台模板
    # return data[0]
    return render_template('admin.html', data=data)


app_bp = Blueprint('app', __name__)


@app_bp.route('')
# @app_bp.route('http://127.0.0.1:5000/')
def index0():
    # Redirect the user to the homepage of app2
    # return redirect(url_for('app2.weiboindex')
    # return redirect('/weiboindex')http://127.0.0.1:5000/
    return redirect('')
    # return redirect('http://127.0.0.1:5000/')

# blueprint2 = Blueprint('blueprint2', __name__, url_prefix='/app2')
# @blueprint2.route('')
# def app2_home():
#     return "This is app2 home page."
# app.register_blueprint(blueprint2)


@app.route('/show')
def show():
    users = Users.query.all()
    return render_template("show_users.html", users=users)

# 国内舆情


@app.route('/guonei')
# def hello_world():  # put application's code here
def guonei():
    return render_template("guonei.html")
# 国外舆情


@app.route('/test_map')
def test_map():
    return render_template("test_map.html")


@app.route('/time')
def getTime():
    return utils.get_time()


@app.route('/queryHotTopicList')
def queryHotTopicList():
    indicators = []
    positiveValues = []
    negativeValues = []
    data = getDatas.queryHotTopicList()
    for item in data:
        indicators.append({"name": item[0], "max": 1})
        positiveValues.append(item[1])
        negativeValues.append(item[2])
    return jsonify({"indicators": indicators, "positiveValues": positiveValues, "negativeValues": negativeValues})


@app.route('/queryStaGender')
def queryStaGender():
    datas = getDatas.querStaGender()
    data = datas[0]
    print(data)
    return jsonify({"maleNum": data[0], "femaleNum": data[1]})


@app.route('/queryStaProvinceDistribute')
def queryStaProvinceDistribute():
    data = getDatas.queryStaProvinceDistribute()
    dataLists = []
    for item in data:
        dataLists.append({
            "name": item[0],
            "value": item[1]
        })
    return jsonify({"dataLists": dataLists})


@app.route('/queryStaWordFrequency')
def queryStaWordFrequency():
    data = getDatas.queryStaWordFrequency()
    dataLists = []
    for item in data:
        dataLists.append({
            "name": item[0],
            "value": item[1]
        })
    return jsonify({"dataLists": dataLists})


@app.route('/queryTopWords')
def queryTopWords():
    data = getDatas.queryTopWords()
    wordNameList = []
    wordNumList = []
    for item in data:
        wordNameList.append(item[0])
        wordNumList.append(item[1])
    wordNumList.reverse()
    wordNameList.reverse()
    return jsonify({"wordNameList": wordNameList, "wordNumList": wordNumList})


@app.route('/queryStaNetizenAttention')
def queryStaNetizenAttention():
    data = getDatas.queryStaNetizenAttention()
    stanaDateList = []
    attentionNumList = []
    for item in data:
        stanaDateList.append(item[1].strftime('%m-%d'))
        attentionNumList.append(item[0])
    return jsonify({"stanaDateList": stanaDateList, "attentionNumList": attentionNumList})


@app.route('/queryTopProvinceDistribute')
def queryTopProvinceDistribute():
    data = getDatas.queryTopProvinceDistribute()
    provinceNameList = []
    sentimentNumList = []
    for item in data:
        provinceNameList.append(item[0])
        sentimentNumList.append(item[1])
    return jsonify({"provinceNameList": provinceNameList, "sentimentNumList": sentimentNumList})

# 不同app泻在同文件
# CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
# conn = pymysql.connect(host='localhost',user='root',password='123456',database='topic',charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor )
# if conn:
#     print('数据库连接成功！')
# else:
#     print('数据库连接失败！')
# app2 = Flask(__name__)
# @app2.route('/weiboindex.html')
# def weiboindex():
#     print(conn)
#     # 从数据库中读取数据
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM weibo')
#     data = cursor.fetchall()
#     # print(data)
#     # #  获取查询结果
#     cursor.close()
#     # # 将数据传递给前台模板
#     # return data[0]
#     return render_template('weiboindex.html', data=data)
#     # resp = jsonify({'message': 'Welcome to somepage!'})
#     # resp.headers['Access-Control-Allow-Origin'] = '*'
#     # return resp


if __name__ == '__main__':
    # app.run(debug=True, port=8000,use_reloader=False)
    app.run(debug=True)
    # 用这个登录注册页面格式不居中了
    # app2.run(debug=True, port=5000,use_reloader=False)

    # app.run(debug=True, port=8000,use_reloader=False)

    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    #     mysql.connection.commit()
    #     cursor.close()
    #     return 'Successfully registered!'
    # else:
    #     return render_template('register.html')

# 改密
# @app.route('/change_password', methods=['GET', 'POST'])
# @login_required
# def change_password():
#     form = ChangePasswordForm()
#     if form.validate_on_submit():
#         if current_user.check_password(form.old_password.data):
#             current_user.set_password(form.new_password.data)
#             db.session.commit()
#             return 'Your password has been updated.'
#         else:
#             return 'Invalid old password'
#     return render_template('change_password.html', form=form)

# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     password_hash = db.Column(db.String(128))

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# 数据库改
# cursor = mysql.connection.cursor()
# cursor.execute('UPDATE users SET username = %s, password = %s WHERE id = %s', (username, password, user_id))
# mysql.connection.commit()
# cursor.close()
# 登出
# Flask-Login提供的 “logout_user” 函数，用户 ID 存储在 Flask-Login提供的 “current_user”，登出既删current_user
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return '你已登出.'
# 改密
# class ChangePasswordForm(FlaskForm):
#     old_password = PasswordField('Old Password', validators=[DataRequired()])
#     new_password = PasswordField('New Password', validators=[
#         DataRequired(),
#         Length(min=6, message='Password must be at least 6 characters.'),
#         EqualTo('confirm_password', message='Passwords must match.')
#     ])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
#     submit = SubmitField('Change Password')
