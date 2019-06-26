from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from database import database_connection
from database.data_schema import users_table
from database.database_connection import Database

database = Database()


@csrf_exempt
def login(request):
    if request.session.__contains__('user_id'):
        del request.session['user_id']
    # while not database.connection.is_connected():
    #     database.connection = database_connection.connect()
    if request.method == 'POST':
        command = request.POST['command']
        if command == 'is_user_exists':
            username = request.POST['username']
            result = users_table.is_user_exists(database.get_connection(), username)
            return HttpResponse(result.__str__())
        if command == 'login':
            username = request.POST['username']
            password = request.POST['password']
            result = users_table.is_password_correct(database.get_connection(), username, password)
            if result:
                user_id = users_table.get_user_id(database.get_connection(), username)
                request.session['user_id'] = user_id
                return HttpResponse(result)
            elif not result:
                return HttpResponse(result)
    return render(request, 'auth/auth.html', {'value': 'login'})


@csrf_exempt
def sign_up(request):
    if request.session.__contains__('user_id'):
        del request.session['user_id']
    if request.method == 'POST':
        command = request.POST['command']
        if command == 'is_user_exists':
            username = request.POST['username']
            result = users_table.is_user_exists(database.get_connection(), username)
            return HttpResponse(result.__str__())
        elif command == 'signup':
            username = request.POST['username']
            password = request.POST['password']
            request.session['user_id'] = users_table.register_user(database.get_connection(), username, password)
            return HttpResponse('True')
    return render(request, 'auth/auth.html', {'value': 'signup'})
