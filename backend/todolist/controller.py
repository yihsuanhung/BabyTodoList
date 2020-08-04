# -*- coding: UTF-8 -*-
from backend.todolist.model import Model


def convert_list_to_dict(l):
    return_list = []
    for i in l:
        data_dict = {"id": i[0], "content": i[1], "status": i[2]}
        return_list.append(data_dict)
    return return_list


class Controller:
    def __init__(self, table_name="TodoListTest", db_name="test.db"):
        self.table_name = table_name
        self.db_name = db_name
        self.model = Model(db_name=self.db_name)

    def create_table(self):
        self.model.create_table(table_name=self.table_name)

    def index(self):
        result = self.model.index(table_name=self.table_name)
        result = convert_list_to_dict(result)
        return result

    def table_length(self):
        result = self.model.table_length(table_name=self.table_name)
        return result

    def paged_index(self, limit, offset):
        result = self.model.paged_index(limit=limit, offset=offset, table_name=self.table_name)
        result = convert_list_to_dict(result)
        return result

    def pagination(self, page, limit):
        db_len = self.table_length()['length']
        offset = limit * (page - 1)
        # find the maximum page number
        if db_len % limit == 0:
            max_page = int(db_len / limit)
        else:
            max_page = int(db_len / limit) + 1
        # print(f"max page for limit={limit}: {max_page} ")
        if page <= max_page:
            result = self.paged_index(limit=limit, offset=offset)
            return {'data': result, 'db_len': db_len, 'code': 0}
        else:
            return {'code': 1, 'data': "no data available"}

    def add_task(self, data, pagination=False, page=None, limit=None):
        result = self.model.add_task(data=data, table_name=self.table_name)
        if result['code'] == 0:
            if (pagination and page!=None and limit!=None):
                return_page = self.pagination(page=page, limit=limit)
                return {'code':0, 'msg':'Success!', 'data': return_page}
            else:
                return_page = self.model.index(table_name=self.table_name)
                return_page = convert_list_to_dict(return_page)
                return {'code':0, 'msg':'Success!', 'data': return_page}
        else:
            return {'code': 1, 'msg': 'Something wrong'}

    def delete_task(self, task_id):
        result = self.model.delete_task(task_id=task_id, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        return_page = convert_list_to_dict(return_page)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def edit_task(self, task_id, data):
        result = self.model.edit_task(task_id=task_id, data=data, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        return_page = convert_list_to_dict(return_page)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def task_done(self, task_id):
        result = self.model.task_done(task_id=task_id, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        return_page = convert_list_to_dict(return_page)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}

    def task_undo(self, task_id):
        result = self.model.task_undo(task_id=task_id, table_name=self.table_name)
        return_page = self.model.index(table_name=self.table_name)
        return_page = convert_list_to_dict(return_page)
        if result['code'] == 0:
            return return_page
        else:
            return {'code': 1, 'msg': 'something wrong'}
