from flask import Flask, jsonify, request, render_template, url_for, redirect
from backend.todolist.controller import Controller
from flask_cors import CORS
import json
# from flask_sqlalchemy import SQLAlchemy
# from forms import SignUpForm
# import cgi

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test_orm.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

CORS(app)
controller = Controller(table_name="TodoListTest")


# html_form = cgi.FieldStorage()
# html_data = html_form.getvalue("content")
# print(html_data)

# 查看
@app.route('/')
def index():
    # return 'TodoList'
    result = controller.index()
    return jsonify(result)


# 檢索（分頁）
@app.route('/index')
def paged_index():
    page = controller.pagination(page=int(request.args['page']), limit=int(request.args['limit']))
    return jsonify(page)


# 新增
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        data = data["content"]
        page = controller.add_task(
            data=data,
            pagination=True,
            page=int(request.args['page']),
            limit=int(request.args['limit'])
        )['data']
        return jsonify(page)

    else:
        return render_template('add.html')


# 刪除
@app.route('/delete/<int:task_id>', methods=['GET', 'DELETE'])
def delete_task(task_id):
    if request.method == 'DELETE':
        controller.delete_task(task_id)
        page = controller.pagination(page=int(request.args['page']), limit=int(request.args['limit']))
        return jsonify(page)

    else:
        err_msg = {'code': 1, 'msg': 'ERROR: please use DELETE method'}
        return jsonify(err_msg)


# 編輯
@app.route('/edit/<int:task_id>', methods=['GET', 'PUT'])
def edit_task(task_id):
    if request.method == 'PUT':
        data = request.get_data()
        data = json.loads(data)
        data = data["content"]
        controller.edit_task(task_id=task_id, data=data)
        page = controller.pagination(page=int(request.args['page']), limit=int(request.args['limit']))
        return jsonify(page)

    else:
        err_msg = {'code': 1, 'msg': 'ERROR: please use PUT method'}
        return jsonify(err_msg)


# 標註為完成
@app.route('/done/<int:task_id>', methods=['GET', 'PUT'])
def task_done(task_id):
    if request.method == 'PUT':
        controller.task_done(task_id)
        page = controller.pagination(page=int(request.args['page']), limit=int(request.args['limit']))
        return jsonify(page)

    else:
        err_msg = {'code': 1, 'msg': 'ERROR: please use PUT method'}
        return jsonify(err_msg)


# 標註為未完成
@app.route('/undo/<int:task_id>', methods=['GET', 'PUT'])
def task_undo(task_id):
    if request.method == 'PUT':
        controller.task_undo(task_id)
        page = controller.pagination(page=int(request.args['page']), limit=int(request.args['limit']))
        return jsonify(page)

    else:
        err_msg = {'code': 1, 'msg': 'ERROR: please use PUT method'}
        return jsonify(err_msg)


@app.route('/count')
def table_length():
    result = controller.table_length()
    return jsonify(result)


@app.route('/create_table')
def create_table():
    controller.create_table()
    return "success"


if __name__ == '__main__':
    app.run()
