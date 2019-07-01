from django.shortcuts import render
from django.views.decorators.cache import cache_page, cache_control

from database.bot_data_schema import general_values_table
from database.data_schema import users_table, news_table
from database.database_connection import Database

database = Database()
telegram_chat_bot_link = general_values_table.get_value(database.get_connection(), "CHAT_BOT_LINK")
telegram_scanner_bot_link = general_values_table.get_value(database.get_connection(), "SCANNER_BOT_LINK")
telegram_chat_link = general_values_table.get_value(database.get_connection(), "CHAT_LINK")

# @cache_page(600, cache='default', key_prefix='')
@cache_control(no_cache=True)
def index(request):
    # while not connection.is_connected():
    #     connection = database_connection.connect()
    #     time.sleep(5000)
    username = ''
    telegram_id = ''
    main_news = news_table.get_last_high_priority_news(database.get_connection())
    secondary_news = news_table.get_three_last_news(database.get_connection(), main_news.news_id)
    if request.session.__contains__('user_id'):
        user_id = request.session['user_id']
        username = users_table.get_username(database.get_connection(), user_id)
        telegram_id = users_table.get_tg_user_id(database.get_connection(), user_id)
    return render(request, 'website/index.html', {
        'username': username,
        'telegram_chat_bot_link': telegram_chat_bot_link,
        'telegram_scanner_bot_link': telegram_scanner_bot_link,
        'telegram_chat_link': telegram_chat_link,
        'telegram_id': telegram_id,
        'main_news': main_news,
        'secondary_news': secondary_news
    })
