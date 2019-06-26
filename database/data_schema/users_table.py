import functools
import operator

from mysql.connector.cursor import MySQLCursorPrepared


def list_users(connection):
    query = "SELECT username FROM data_schema.users"
    cursor = connection.cursor()
    cursor.execute(query)
    for username in cursor:
        str_username = functools.reduce(operator.add, username)
        print(str_username)


def is_user_exists(connection, username):
    username = str.lower(username)
    query = """SELECT username FROM data_schema.users WHERE username=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (username,))

    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True


def is_password_correct(connection, username, password):
    username = str.lower(username)
    password = password.encode('utf-8')
    # password = hashlib.md5(password).hexdigest()
    query = """SELECT username FROM data_schema.users WHERE username=%s AND password=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (username, password,))

    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True


def get_user_id(connection, username):
    username = str.lower(username)
    query = """SELECT user_id FROM data_schema.users WHERE username=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (username,))
    data = cursor.fetchall()
    return functools.reduce(operator.add, data[0])


def get_username(connection, user_id):
    query = """SELECT username FROM data_schema.users WHERE user_id=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    if len(data) > 0:
        return functools.reduce(operator.add, data[0])
    else:
        return ''


def get_tg_user_id(connection, user_id):
    query = """SELECT chat_id FROM data_schema.users WHERE user_id=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    if len(data) > 0:
        return functools.reduce(operator.add, data[0])
    else:
        return ''


def register_user(connection, username, password):
    query = """INSERT INTO data_schema.users (username, password) VALUES (%s, %s)"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (username, password,))
    connection.commit()
    return cursor.lastrowid
