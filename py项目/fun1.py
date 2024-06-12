# _*_ coding : utf-8 _*_
# @Time : 2024/6/1 13:50
# @Author : xl
# @File : fun1
# @Project : yy
import csv
import os
import pyodbc
from flask import Flask, render_template, request, redirect, url_for, flash
#csv文件名
USER_DATA_CSV = 'users.csv'
#创建csv文件
def createcsv():
    if not os.path.exists(USER_DATA_CSV):
        with open(USER_DATA_CSV, 'w', newline='') as csvfile:
            fieldnames = ['username', 'password']  # 示例字段
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
#写入csv
def write_to_csv(username, password):
    with open(USER_DATA_CSV, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, password])
#首页功能
def index_fun():
    if request.method == 'POST':
        # 处理登录逻辑...
        # 如果登录成功，重定向到主页或其他页面
        return redirect(url_for('index'))
    # 否则，渲染登录页面模板
    return render_template('index.html')
#注册功能
def register_fun():
    if request.method == 'POST':
        # 从表单中获取用户名和密码
        username = request.form['username']
        password = request.form['password']
        username=username.strip();
        password=password.strip();
        if username=="":
            flash('未填写用户名！')
        elif password=="":
            flash('未填写密码！')
        elif check_register(username):
            flash('用户名已经存在！')
        else:
            write_to_csv(username, password)
            flash('用户注册成功，请登录！')
            #return redirect(url_for('index'))
    # 如果是GET请求，则渲染注册页面
    return render_template('register.html')
#注册用户名验证
def check_register(username):
    with open(USER_DATA_CSV, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                return True
    return False
#登录功能
def login_fun():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            # 在这里设置会话或执行其他登录后操作
            flash('登录成功!')
            return redirect(url_for('index'))  # 假设有一个名为'index'的路由
        else:
            flash('登录名或密码错误！')
    return render_template('login.html')

#登录用户名、密码验证
def check_login(username, password):
    with open(USER_DATA_CSV, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False


#关于我们功能
def about_fun():
    return render_template('about.html')






#读取调查问卷中的问题
def read_questions_from_csv(filename):
    import ast
    questions = []
    with open(filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            question_id = row['id']
            question_text = row['question']
            options = ast.literal_eval(row['options'])
            questions.append({'id': question_id,
                    'text': question_text, 'options': options})
    return questions
#调查问卷路由
def survey_fun():
    questions = read_questions_from_csv('questions.csv')
    return render_template('survey.html', questions=questions)
#调查问卷提交路由
def survey_submit_fun():
    from datetime import datetime
    # 创建一个字典来存储所有答案
    answers = {}\

    CSVFilename1="questions.csv"
    CSVFilename2 = "answers.csv"
    # 遍历所有的问题 ID，并获取对应的答案
    for question_id in range(1, len(read_questions_from_csv(CSVFilename1)) + 1):  # 假设问题 ID 是连续的
        question_key = f'question_{question_id}'
        if question_key in request.form:
            # 获取选中的选项
            answer = request.form[question_key]
            # 将答案存储在字典中，使用问题 ID 作为键
            answers[question_id] = answer
    # 将答案保存到 CSV 文件中（例如 "answers.csv"）
    fieldnames = ['question_id', 'answer', 'time']  # 示例字段
    if not os.path.exists(CSVFilename2):
        with open(CSVFilename2, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(CSVFilename2, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for question_id, answer in answers.items():
            writer.writerow({'question_id': question_id, 'answer': answer,'time':datetime.now() })

            # 重定向到另一个页面或显示成功消息
    return redirect(url_for('success'))
#调查问卷提交成功显示结果路由
def success_fun():
    import plotly.graph_objects as go
    from plotly.io import to_html

    CSVFilename1 = "questions.csv"
    CSVFilename2 = "answers.csv"
    answers = []
    with open(CSVFilename2, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            question_id = row['question_id']
            answer_text = row['answer']
            answers.append({'question_id': question_id, 'answer': answer_text})
    questions = read_questions_from_csv(CSVFilename1)

    htmls=[]
    str1="https://cdn.plot.ly/plotly-2.32.0.min.js"
    str2="/static/js/plotly-latest.min.js"
    for question in questions:
        labels=question['options']
        values=[]
        for label in labels:
            n1 = 0
            for answer in answers:
                if answer['question_id'] == question["id"] and label==answer["answer"]:
                    n1+=1
            values.append(n1)
        #print(labels,values)
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title_text=question['text'])
        # 将图表转换为HTML
        graph_html = to_html(fig, include_plotlyjs='cdn')
        graph_html.replace(str1, str2)

        htmls.append(graph_html)

    return render_template("success.html",graphs=htmls)
