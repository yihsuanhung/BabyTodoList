# -*- coding: UTF-8 -*-
import sqlite3


class Model:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.c = self.conn.cursor()

        print('Get DataBase Connect!')

    def index(self, table_name):
        sql_exe = f"select * from {table_name};"
        result = self.c.execute(sql_exe).fetchall()
        return result

    def create_table(self, table_name="TodoList"):
        sql_exe = f"""CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            content CHAR NOT NULL,
            status BOOL DEFAULT FALSE NOT NULL);"""
        self.c.execute(sql_exe)
        self.conn.commit()
        # self.conn.close

    def add_task(self, table_name, data):
        sql_exec = f"insert into {table_name}(content) values('{str(data)}');"
        self.c.execute(sql_exec)
        self.conn.commit()
        print(f'insert data: {str(data)} to {table_name}')
        code = {'code': 0, 'msg': 'insert success!'}
        return code

    def delete_task(self, table_name, task_id):
        sql_exe = f"delete from {table_name} where id = {task_id};"
        self.c.execute(sql_exe)
        self.conn.commit()
        print(f'delete data: id={task_id} from {table_name}')
        code = {'code': 0, 'msg': 'delete success!'}
        return code

    def edit_task(self, table_name, task_id, data):
        sql_exe = f"update {table_name} set content = '{str(data)}' where id = {task_id};"
        self.c.execute(sql_exe)
        self.conn.commit()
        print(f'edit data: id={task_id} from {table_name}')
        code = {'code': 0, 'msg': 'edit success!'}
        return code

    def task_done(self, table_name=None, task_id=None):
        sql_exe = f"update {table_name} set status = true where id = {task_id};"
        self.c.execute(sql_exe)
        self.conn.commit()
        print(f'mark data: id={task_id} as done')
        code = {'code': 0, 'msg': 'task done'}
        return code

    def task_undo(self, table_name=None, task_id=None):
        sql_exe = f"update {table_name} set status = false where id = {task_id};"
        result = self.do_exec(sql_exe)
        print(f'mark data: id={task_id} as undo')
        return result

    def table_length(self, table_name=None):
        sql_exe = f"select count(0) from {table_name};"
        self.c.execute(sql_exe)
        result = self.c.fetchone()[0]
        # print(f'count length of table, {table_name}: {result}')
        code = {'code': 0, 'length': result}
        return code

    def paged_index(self, limit, offset, table_name=None):
        sql_exe = f"select * from {table_name} order by id DESC limit {limit} offset {offset};"
        result = self.c.execute(sql_exe).fetchall()
        # print("pagination")
        return result
        # self.find({'data':{},'limit':5,'add'})

    def find(self):
        pass

    # def edit_on(self, table_name=None, task_id=None):
    #     sql_exe = f"update {table_name} set editstat = true where id = {task_id};"
    #     result = self.do_exec(sql_exe)
    #     print(f'turn edit status on, data: id={task_id}')
    #     return result
    #
    # def edit_off(self, table_name=None, task_id=None):
    #     sql_exe = f"update {table_name} set editstat = false where id = {task_id};"
    #     result = self.do_exec(sql_exe)
    #     print(f'turn edit status off, data: id={task_id}')
    #     return result

    def do_exec(self, sql):  # 封裝exec
        try:
            self.c.execute(sql)
            self.conn.commit()
            code = {'code': 0, 'msg': 'task undo!'}
            return code
        except Exception as err:
            return {'code': 1, 'msg': err}

    # def crud(self, table_name="TodoList", action_type=None, task_id=None, data=None):
    #     if action_type == 'add_task':
    #         sql_exe = f"insert into {table_name}(content) values('{str(data)}');"
    #     elif action_type == 'delete_task':
    #         sql_exe = f"delete from {table_name} where id = {task_id};"
    #     elif action_type == 'edit_task':
    #         sql_exe = f"update {table_name} set content = '{str(data)}' where id = {task_id};"
    #     elif action_type == 'task_done':
    #         sql_exe = f"update {table_name} set status = true where id = {task_id};"
    #     elif action_type == 'task_undo':
    #         sql_exe = f"update {table_name} set status = false where id = {task_id};"
    #     else:
    #         sql_exe = ""
    #
    #     self.c.execute(sql_exe)
    #     self.conn.commit()
    #     code = {'code': 0, 'msg': 'success!'}
    #     return code
