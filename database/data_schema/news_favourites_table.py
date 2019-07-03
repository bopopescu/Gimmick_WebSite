from multiprocessing.sharedctypes import synchronized

from mysql.connector.cursor import MySQLCursorPrepared


def add_to_favourites(connection, news_id, user_id):
    if not is_in_favourites(connection, news_id, user_id):
        query = """INSERT INTO data_schema.news_favourites (news_id, user_id) VALUES (%s, %s)"""
        cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
        cursor.execute(query, (news_id, user_id,))
        connection.commit()
        return True


def remove_from_favourites(connection, news_id, user_id):
    query = """DELETE FROM data_schema.news_favourites WHERE news_id=%s AND user_id=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (news_id, user_id,))
    connection.commit()
    return True


def is_in_favourites(connection, news_id, user_id):
    query = """SELECT user_id FROM data_schema.news_favourites WHERE news_id=%s AND user_id=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (news_id, user_id,))

    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True
