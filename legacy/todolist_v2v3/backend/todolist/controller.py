# -*- coding: UTF-8 -*-
from backend.todolist.model import Model


class Controller:
    def __init__(self, table_name="TodoListTest", db_name="test.db"):
        self.table_name = table_name
        self.db_name = db_name
        self.model = Model(db_name=self.db_name)

    def create_table(self):
        self.model.create_table(table_name=self.table_name)

    def index(self):
        result = self.model.index(table_name=self.table_name)
        return result

    def add_task(self, data):
        result = self.model.add_task(data=data, table_name=self.table_name)
        if result['code'] == 0:
            return_page = self.model.index(table_name=self.table_name)
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def delete_task(self, task_id):
        result = self.model.delete_task(task_id=task_id, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def edit_task(self, task_id, data):
        result = self.model.edit_task(task_id=task_id, data=data, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def task_done(self, task_id):
        result = self.model.task_done(task_id=task_id, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def task_undo(self, task_id):
        result = self.model.task_undo(task_id=task_id, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def edit_on(self, task_id):
        result = self.model.edit_on(task_id=task_id, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def edit_off(self, task_id):
        result = self.model.edit_off(task_id=task_id, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}
