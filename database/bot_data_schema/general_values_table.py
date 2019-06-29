import functools
import operator

from mysql.connector.cursor import MySQLCursorPrepared


def get_value(connection, signature):
    query = """SELECT value FROM bot_data_schema.general_values WHERE signature=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (signature,))
    data = cursor.fetchall()
    if len(data) > 0:
        return functools.reduce(operator.add, data[0])
    else:
        return ''
