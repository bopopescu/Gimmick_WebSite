import functools
import operator

from mysql.connector.cursor import MySQLCursorPrepared


def get_avatar_link(connection, user_id):
    query = """SELECT avatar_link FROM data_schema.users_information WHERE db_user_id=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    if len(data) > 0:
        return functools.reduce(operator.add, data[0])
    else:
        return ''
