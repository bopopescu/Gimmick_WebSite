import json
import socket
import threading

import websockets as websockets
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from database.database_connection import Database

from tornado import websocket
import tornado.ioloop

database = Database()


class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print("Websocket Opened")

    def on_message(self, message):
        self.write_message(u"You said: %s" % message)

    def on_close(self):
        print ("Websocket closed")


application = tornado.web.Application([(r"/", EchoWebSocket), ])





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

application.listen(9000)
tornado.ioloop.IOLoop.instance().start()


def check_updates():
    global updates
    print("9000 socket")

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