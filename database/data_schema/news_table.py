import functools
import hashlib
import operator

from mysql.connector.cursor import MySQLCursorPrepared

from database import news
from database.news import News


def get_last_high_priority_news(connection):
    query = """SELECT id, title, block_1, date FROM data_schema.news WHERE priority=1 ORDER BY id DESC"""
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    n = News()

    for row in data:
        n.news_id = row[0]
        n.title = row[1]
        n.text = row[2]
        n.date = row[3]
        n.image_link = get_news_main_image_link(connection, n.news_id)
        break
    n.favourites = get_news_favourites(connection, n.news_id)
    if len(data) > 0:
        return n
    else:
        return ''


def get_news_favourites(connection, news_id):
    query = """SELECT news_id FROM data_schema.news_favourites WHERE news_id=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (news_id,))
    data = cursor.fetchall()
    return len(data)


def get_news_main_image_link(connection, news_id):
    query = """SELECT (link) FROM data_schema.news_images WHERE news_id=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (news_id,))
    data = cursor.fetchall()
    for row in data:
        return row[0]
    return ''


def get_tree_last_news(connection, high_priority_id):
    query = """SELECT id, title, block_1, date FROM data_schema.news WHERE id!=%s ORDER BY id DESC"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (high_priority_id,))
    data = cursor.fetchall()
    news_list = [News(), News(), News()]
    i = 0
    for row in data:
        if i == 3:
            break
        news_list[i].news_id = row[0]
        news_list[i].title = row[1]
        news_list[i].text = row[2]
        news_list[i].date = row[3]
        news_list[i].image_link = get_news_main_image_link(connection, news_list[i].news_id)
        news_list[i].favourites = get_news_favourites(connection, news_list[i].news_id)
        i += 1
    return news_list
