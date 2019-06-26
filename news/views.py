from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from database import database_connection
from database.data_schema import news_table
from database.database_connection import Database

database = Database()


@csrf_exempt
def news(request):
    # if not request.session.__contains__('user_id'):
    #     return render(request, 'news/error.html')

    # while not database.connection.is_connected():
    #     connection = database_connection.connect()

    news_id = 0
    if request.method == 'GET':
        news_id = request.GET['news_id']
    news_full = news_table.get_full_news_by_id(database.get_connection(), news_id)
    return render(request, 'news/news.html', {'news_full': news_full})
