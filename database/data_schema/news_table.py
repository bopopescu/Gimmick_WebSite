from mysql.connector.cursor import MySQLCursorPrepared

from database.objects.news import News, NewsFull, Block


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
        n.image_link = get_news_main_images_links(connection, n.news_id, 0)[0]
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


def get_news_main_images_links(connection, news_id, block):
    query = """SELECT (link) FROM data_schema.news_images WHERE news_id=%s AND block=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (news_id, block,))
    data = cursor.fetchall()
    images = []
    for row in data:
        images.append(row[0])
    return images


def get_three_last_news(connection, high_priority_id):
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
        news_list[i].image_link = get_news_main_images_links(connection, news_list[i].news_id, 0)[0]
        news_list[i].favourites = get_news_favourites(connection, news_list[i].news_id)
        i += 1
    return news_list


def get_full_news_by_id(connection, news_id):
    query = """SELECT id, title, date, block_1, block_2, block_3, block_4, block_5, block_6, block_7 FROM data_schema.news WHERE id=%s"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (news_id,))
    data = cursor.fetchall()
    news_full = NewsFull()
    news_full.blocks.append(Block())
    news_full.blocks.append(Block())
    news_full.blocks.append(Block())
    news_full.blocks.append(Block())
    news_full.blocks.append(Block())
    news_full.blocks.append(Block())
    news_full.blocks.append(Block())
    for row in data:
        news_full.news_id = row[0]
        news_full.title = row[1]
        news_full.date = row[2]
        news_full.blocks[0].text = row[3]
        news_full.blocks[1].text = row[4]
        news_full.blocks[2].text = row[5]
        news_full.blocks[3].text = row[6]
        news_full.blocks[4].text = row[7]
        news_full.blocks[5].text = row[8]
        news_full.blocks[6].text = row[9]
        news_full.blocks[0].images = get_news_main_images_links(connection, news_id, 1)
        news_full.blocks[1].images = get_news_main_images_links(connection, news_id, 2)
        news_full.blocks[2].images = get_news_main_images_links(connection, news_id, 3)
        news_full.blocks[3].images = get_news_main_images_links(connection, news_id, 4)
        news_full.blocks[4].images = get_news_main_images_links(connection, news_id, 5)
        news_full.blocks[5].images = get_news_main_images_links(connection, news_id, 6)
        news_full.blocks[6].images = get_news_main_images_links(connection, news_id, 7)
    news_full.main_image_link = get_news_main_images_links(connection, news_id, 0)[0]
    news_full.favourites = get_news_favourites(connection, news_full.news_id)
    return news_full

