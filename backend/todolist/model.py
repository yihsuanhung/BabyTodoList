# -*- coding: UTF-8 -*-
import sqlite3


class Model:
    def __init__(self, db_name):
        self.db_name = db_name
        try:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.c = self.conn.cursor()
            print('Get DataBase Connect!')
        except Exception as e:
            print("[DataBase Connection Error]", e)

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
        try:
            self.c.execute(sql_exec)
            self.conn.commit()
            print(f'insert data: {str(data)} to {table_name}')
            return {'code': 0, 'msg': 'insert success!'}
        except Exception as e:
            print("[Error in adding task]", e)
            return {'code': 1, 'msg': 'Something wrong'}

    def delete_task(self, table_name, task_id):
        sql_exe = f"delete from {table_name} where id = {task_id};"
        try:
            self.c.execute(sql_exe)
            self.conn.commit()
            print(f'delete data: id={task_id} from {table_name}')
            return {'code': 0, 'msg': 'delete success!'}
        except Exception as e:
            print("[Error in deleting task]", e)
            return {'code': 1, 'msg': 'Something wrong'}

    def edit_task(self, table_name, task_id, data):
        sql_exe = f"update {table_name} set content = '{str(data)}' where id = {task_id};"
        try:
            self.c.execute(sql_exe)
            self.conn.commit()
            print(f'edit data: id={task_id} from {table_name}')
            return {'code': 0, 'msg': 'edit success!'}
        except Exception as e:
            print("[Error in editing]", e)
            return {'code': 1, 'msg': 'Something wrong'}

    def task_done(self, table_name=None, task_id=None):
        sql_exe = f"update {table_name} set status = true where id = {task_id};"
        try:
            self.c.execute(sql_exe)
            self.conn.commit()
            print(f'mark data: id={task_id} as done')
            code = {'code': 0, 'msg': 'task done'}
            return code
        except Exception as e:
            print("[Error in marking tasks as done]", e)
            return {'code': 1, 'msg': 'Something wrong'}

    def task_undo(self, table_name=None, task_id=None):
        sql_exe = f"update {table_name} set status = false where id = {task_id};"
        try:
            result = self.do_exec(sql_exe)
            print(f'mark data: id={task_id} as undo')
            return result
        except Exception as e:
            print("[Error in marking tasks as undo]", e)
            return {'code': 1, 'msg': 'Something wrong'}

    def table_length(self, table_name=None):
        sql_exe = f"select count(0) from {table_name};"
        try:
            self.c.execute(sql_exe)
            result = self.c.fetchone()[0]
            return {'code': 0, 'length': result}
        except Exception as e:
            print("[Error in counting table length]", e)
            return {'code': 1, 'msg': 'Something wrong'}

    def paged_index(self, limit, offset, table_name=None):
        sql_exe = f"select * from {table_name} order by id DESC limit {limit} offset {offset};"
        try:
            return self.c.execute(sql_exe).fetchall()
        except Exception as e:
            print("[Error in indexing]", e)
            return {'code': 1, 'msg': 'Something wrong'}

    def find(self):
        pass

    def do_exec(self, sql):  # 封裝exec
        try:
            self.c.execute(sql)
            self.conn.commit()
            code = {'code': 0, 'msg': 'task undo!'}
            return code
        except Exception as err:
            return {'code': 1, 'msg': err}
