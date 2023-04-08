class Users(db.Model):
    __tablename__ = 'users'
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(50), unique=True, nullable=False)
password = db.Column(db.String(255), nullable=False)
# 添加密码哈希方法
def set_password(self, password):
    self.password_hash = generate_password_hash(password)
# 添加密码校验方法
def check_password(self, password):
    return check_password_hash(self.password_hash, password)
