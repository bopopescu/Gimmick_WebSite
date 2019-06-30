import datetime
import threading

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
import json
import socket

from database.data_schema import users_information_table
from database.database_connection import Database

database = Database()

connect = {
    'command': 'connect',
    'value': 'website',
}

sock = socket.socket()
sock.connect(('localhost', 8174))
string = json.dumps(connect) + '\n'
sock.send(string.encode())
data = sock.recv(1024)
result = json.loads(data)

updates = []


def check_updates():
    global updates
    while True:
        inp = sock.recv(1024)
        updates.append(inp)
        print(inp)
        print(len(updates))


if result['value'] == 'connected':
    thread = threading.Thread(target=check_updates, args=())
    thread.start()


@csrf_exempt
def index(request):
    if not request.session.__contains__('user_id'):
        return render(request, 'auth/auth.html', {
            'page': 'login',
            'message': 'Вы должны войти в систему либо зарегестрироваться чтобы общаться с другими пользователями'
        })

    return render(request, 'chat/chat.html', {
        'current_user_id': request.session['user_id']
    })


@csrf_exempt
@cache_control(no_cache=True)
def update(request):
    print(request.POST['command'])
    current_id = int(request.POST['current_id'])
    print(current_id)
    global updates
    if not request.session.__contains__('user_id'):
        return render(request, 'auth/auth.html', {
            'page': 'login',
            'message': 'Вы должны войти в систему либо зарегестрироваться чтобы общаться с другими пользователями'
        })
    if request.method == 'POST':
        if request.POST['command'] == 'get-last-id':
            return HttpResponse(len(updates))
        elif request.POST['command'] == 'new-update':
            if len(updates) > int(request.POST['current_id']):
                current_id = int(request.POST['current_id'])
                decrypted_update = json.loads(updates[current_id])
                if decrypted_update['command'] == 'new-message':
                    message = json.loads(decrypted_update['value'])
                    response = json.dumps(
                        {
                            'update_id': current_id,
                            'command': 'new-message',
                            'userId': message['userId'],
                            'message_text': message['messageText'],
                            'avatar_link': users_information_table.get_avatar_link(database.get_connection(), message['userId']),
                            'message_time': datetime.datetime.fromtimestamp(message['time'] / 1000.0).strftime("%H:%M:%S - %b %d %Y")
                        }
                    )
                    # str_time = datetime.datetime.fromtimestamp(message['time'] / 1000.0).strftime("%H:%M:%S - %b %d %Y")
                    # response = json.dumps(
                    #     {
                    #         'new-message', message['userId'], message['messageText'],
                    #         users_information_table.get_avatar_link(database.get_connection(), message['userId']),
                    #         "blablabla"
                    #     }
                    # )
                    return HttpResponse(response)
    return HttpResponse("")
