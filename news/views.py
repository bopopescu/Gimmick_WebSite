from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from database import database_connection
from database.data_schema import news_table, news_favourites_table
from database.database_connection import Database

database = Database()


@csrf_exempt
@cache_control(no_cache=True)
def news(request):
    if not request.session.__contains__('user_id'):
        return render(request, 'auth/auth.html', {
            'page': 'login',
            'message': 'Вы должны войти в систему либо зарегестрироваться чтобы '
                       'получить возможность насладиться новостью'
        })
    news_id = 0
    if request.method == 'GET':
        news_id = request.GET['news_id']
    if request.method == 'POST':
        if request.POST['command'] == 'change-favourites':
            user_id = request.session['user_id']
            if user_id == 0:
                return HttpResponse('false')
            news_id = request.POST['news_id']
            if not news_favourites_table.is_in_favourites(database.get_connection(), news_id, user_id):
                if news_favourites_table.add_to_favourites(database.get_connection(), news_id, user_id):
                    return HttpResponse('+' + news_table.get_news_favourites(database.get_connection(), news_id).__str__())
                else:
                    return HttpResponse('false')
            else:
                if news_favourites_table.remove_from_favourites(database.get_connection(), news_id, user_id):
                    return HttpResponse('-' + news_table.get_news_favourites(database.get_connection(), news_id).__str__())
                else:
                    return HttpResponse('false')
    news_full = news_table.get_full_news_by_id(database.get_connection(), news_id, request.session['user_id'])
    return render(request, 'news/news_single.html', {'news_full': news_full})
    # while not database.connection.is_connected():
    #     connection = database_connection.connect()
