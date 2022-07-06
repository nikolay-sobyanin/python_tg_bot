from peewee import *

DB = SqliteDatabase('database/history.db')
TABLE_NAME = 'History Users'


class HistoryUsers(Model):
    user_id = IntegerField()
    name_cmd = CharField()
    time_cmd = DateTimeField()
    hotels = CharField()

    class Meta:
        database = DB
        db_table = TABLE_NAME


db_table = HistoryUsers
if TABLE_NAME not in DB.get_tables():
    db_table.create_table()


def add_row(user_id: int, name_cmd: str, time_cmd: str, hotels: str) -> None:
    db_table.create(user_id=user_id, name_cmd=name_cmd, time_cmd=time_cmd, hotels=hotels)


def get_user_history(user_id: int, count_rows: int) -> list:
    history = list()
    for row in db_table.select().where(db_table.user_id == user_id).order_by(db_table.time_cmd):
        history.append({'name_cmd': row.name_cmd, 'time_cmd': row.time_cmd, 'hotels': row.hotels})
        if len(history) == count_rows:
            return history
    return history

