from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'chat/chat.html')


@csrf_exempt
def update(request):
    print(request.POST['command'])
    return HttpResponse()
