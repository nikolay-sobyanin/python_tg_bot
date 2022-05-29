import sqlite3


class ControlState:
    TABLE_NAME = 'states'
    COLUMN = ['user_id', 'command', 'state']

    def __init__(self, path_db: str):
        self.path_db = path_db

    def __connect_db(self):
        connection = sqlite3.connect(self.path_db)
        cursor = connection.cursor()
        return connection, cursor

    def set_state(self, user_id: int, command: str, step: str):
        connection, cursor = self.__connect_db()
        sql_query = f'INSERT INTO {self.TABLE_NAME} VALUES(?, ?, ?);'
        cursor.execute(sql_query, (user_id, command, step))
        connection.commit()
        connection.close()

    def change_step(self, user_id: int, step: str):
        connection, cursor = self.__connect_db()
        sql_query = f'UPDATE {self.TABLE_NAME} SET {self.COLUMN[2]} = {step} WHERE {self.COLUMN[0]} = {user_id};'
        cursor.execute(sql_query)
        connection.commit()
        connection.close()

    def del_state(self, user_id):
        connection, cursor = self.__connect_db()
        sql_query = f'DELETE FROM {self.TABLE_NAME} WHERE {self.COLUMN[0]} = {user_id}'
        cursor.execute(sql_query)
        connection.commit()
        connection.close()

    def get_state(self, user_id):
        connection, cursor = self.__connect_db()
        sql_query = f'SELECT {self.COLUMN[1]} {self.COLUMN[2]} FROM {self.TABLE_NAME} WHERE {self.COLUMN[0]} = {user_id}'
        cursor.execute(sql_query)
        command, step = cursor.fetchone()
        connection.close()
        return command, step
