from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error
from jinja2 import Template
app = Flask(__name__)
# MySQL连接设置
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="mydatabase"
)
# 用户类
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
# 获取所有用户
def get_all_users():
    users = []
    try:
        # 查询所有用户
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        # 将查询结果转换为用户对象列表
        for row in result:
            user = User(row[0], row[1], row[2])
            users.append(user)
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        cursor.close()
    return users
# 根据ID获取用户
def get_user_by_id(id):
    try:
        # 根据ID查询用户
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        result = cursor.fetchone()
        # 如果查询结果不为空，则返回用户对象
        if result:
            user = User(result[0], result[1], result[2])
            return user
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        cursor.close()
    return None
# 添加用户
def add_user(name, email):
    try:
        # 插入新用户
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        mydb.commit()
    except Error as e:
        print("Error writing data to MySQL table", e)
        mydb.rollback()
    finally:
        cursor.close()
# 更新用户
def update_user(id, name, email):
    try:
        # 更新用户信息
        cursor = mydb.cursor()
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id))
        mydb.commit()
    except Error as e:
        print("Error writing data to MySQL table", e)
        mydb.rollback()
    finally:
        cursor.close()
# 删除用户
def delete_user(id):
    try:
        # 删除用户
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        mydb.commit()
    except Error as e:
        print("Error writing data to MySQL table", e)
        mydb.rollback()
    finally:
        cursor.close()
# 显示所有用户
@app.route("/")
def index():
    users = get_all_users()
    return render_template("index.html", users=users)
# 显示添加用户页面
@app.route("/add")
def add():
    return render_template("add.html")
# 处理添加用户请求
@app.route("/add", methods=["POST"])
def add_post():
    name = request.form["name"]
    email = request.form["email"]
    add_user(name, email)
    return redirect("/")
# 显示编辑用户页面
@app.route("/edit/<int:id>")
def edit(id):
    user = get_user_by_id(id)
    return render_template("edit.html", user=user)
# 处理编辑用户请求
@app.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    name = request.form["name"]
    email = request.form["email"]
    update_user(id, name, email)
    return redirect("/")
# 处理删除用户请求
@app.route("/delete/<int:id>")
def delete(id):
    delete_user(id)
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)