# import asyncio
# import json
# import socket
# import threading
#
# import websockets as websockets
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
#
# from database.database_connection import Database
#
# database = Database()
#
#
# connect = {
#     'command': 'connect',
#     'value': 'website',
# }
#
# sock = socket.socket()
# sock.connect(('localhost', 8174))
# string = json.dumps(connect) + '\n'
# sock.send(string.encode())
# data = sock.recv(1024)
# result = json.loads(data)
#
# updates = []
#
# websockets_ls = []
#
#
# async def response(websocket, path):
#     if not websockets_ls.__contains__(websocket):
#         websockets_ls.append(websocket)
#     while True:
#         message = await websocket.recv()
#         for w in websockets_ls:
#             print(w)
#             w.send("Message has been rec.")
#         print(message)
#         print("Bla bla " + message)
#         await websocket.send("Message has been rec..")
#
#
# def check_updates():
#     global updates
#
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     start_server = websockets.serve(response, 'localhost', 9000)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()
#
#     while True:
#         inp = sock.recv(1024)
#         updates.append(inp)
#         print(inp)
#         print(len(updates))
#
#
# if result['value'] == 'connected':
#     thread = threading.Thread(target=check_updates, args=())
#     thread.start()
#
#
# @csrf_exempt
# def index(request):
#     if not request.session.__contains__('user_id'):
#         return render(request, 'auth/auth.html', {
#             'page': 'login',
#             'message': 'Вы должны войти в систему либо зарегестрироваться чтобы общаться с другими пользователями'
#         })
#
#     return render(request, 'chat/chat.html', {
#         'current_user_id': request.session['user_id']
#     })