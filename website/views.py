import time

from django.http import HttpResponse
from django.shortcuts import render

from database import database_connection
from database.data_schema import users_table, news_table
from database.bot_data_schema import general_values_table

connection = database_connection.connect()


def index(request):
    global connection
    # while not connection.is_connected():
    #     connection = database_connection.connect()
    #     time.sleep(5000)
    username = ''
    telegram_chat_bot_link = general_values_table.get_value(connection, "CHAT_BOT_LINK")
    telegram_scanner_bot_link = general_values_table.get_value(connection, "SCANNER_BOT_LINK")
    telegram_chat_link = general_values_table.get_value(connection, "CHAT_LINK")
    telegram_id = ''
    main_news = news_table.get_last_high_priority_news(connection)
    secondary_news = news_table.get_tree_last_news(connection, main_news.news_id)
    print(secondary_news[0].news_id)
    print(secondary_news[1].news_id)
    print(secondary_news[2].news_id)
    if request.session.__contains__('user_id'):
        user_id = request.session['user_id']
        username = users_table.get_username(connection, user_id)
        telegram_id = users_table.get_tg_user_id(connection, user_id)
    return render(request, 'website/index.html', {
        'username': username,
        'telegram_chat_bot_link': telegram_chat_bot_link,
        'telegram_scanner_bot_link': telegram_scanner_bot_link,
        'telegram_chat_link': telegram_chat_link,
        'telegram_id': telegram_id,
        'main_news': main_news,
        'secondary_news': secondary_news
    })
