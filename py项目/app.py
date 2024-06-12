# _*_ coding : utf-8 _*_
# @Time : 2024/6/1 13:44
# @Author : xl
# @File : app
# @Project : yy

from fun1 import *


app = Flask(__name__)
app.secret_key = 'your-secret-key'
#创建csv文件，用于存储用户名和密码
createcsv()

#首页路由
@app.route('/')
def index():
    return index_fun()
#注册页路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_fun()
#登录页路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    return(login_fun())
#关于我们页路由
@app.route('/about', methods=['GET'])
def about():
    return(about_fun());






#问卷调查路由
@app.route('/survey', methods=['GET'])
def survey():
    return(survey_fun());
#问卷调查提交路由
@app.route('/survey_submit', methods=['POST'])
def survey_submit():
    return(survey_submit_fun());
#问卷调查路由成功路由
@app.route('/success', methods=['GET'])
def success():
    return(success_fun());



if __name__ == '__main__':
    app.run(debug=True)
