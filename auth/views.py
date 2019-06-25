from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from database import database_connection
from database.data_schema import users_table

connection = database_connection.connect()


@csrf_exempt
def login(request):
    if request.session.__contains__('user_id'):
        del request.session['user_id']
    global connection
    while not connection.is_connected():
        connection = database_connection.connect()
    if request.method == 'POST':
        command = request.POST['command']
        if command == 'is_user_exists':
            username = request.POST['username']
            result = users_table.is_user_exists(connection, username)
            return HttpResponse(result.__str__())
        if command == 'login':
            username = request.POST['username']
            password = request.POST['password']
            result = users_table.is_password_correct(connection, username, password)
            if result:
                user_id = users_table.get_user_id(connection, username)
                request.session['user_id'] = user_id
                return HttpResponse(result)
            elif not result:
                return HttpResponse(result)
    return render(request, 'auth/auth.html', {'value': 'login'})


@csrf_exempt
def sign_up(request):
    if request.session.__contains__('user_id'):
        del request.session['user_id']
    global connection
    if request.method == 'POST':
        command = request.POST['command']
        if command == 'is_user_exists':
            username = request.POST['username']
            result = users_table.is_user_exists(connection, username)
            return HttpResponse(result.__str__())
        elif command == 'signup':
            username = request.POST['username']
            password = request.POST['password']
            request.session['user_id'] = users_table.register_user(connection, username, password)
            return HttpResponse('True')
    return render(request, 'auth/auth.html', {'value': 'signup'})
