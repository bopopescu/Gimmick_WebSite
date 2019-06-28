import datetime
import threading

from django.http import HttpResponse
from django.shortcuts import render
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
    while True:
        global updates
        inp = sock.recv(1024)
        updates.append(inp)


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
def update(request):
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
                print(updates[current_id])
                if decrypted_update['command'] == 'new-message':
                    message = json.loads(decrypted_update['value'])
                    print(message['time'])
                    return HttpResponse("""{
                        'command': 'new-message',
                        'userId': message['userId'],
                        'message_text': message['messageText'],
                        'avatar_link': users_information_table.get_avatar_link(database.get_connection(),
                                                                               message['userId']),
                        'message_time': datetime.datetime.fromtimestamp(int(message['time']) / 1000.0)
                    }""")
