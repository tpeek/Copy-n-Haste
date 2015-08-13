from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import redis

with open("typing_test/test1.txt", "r") as myfile:
    data2 = myfile.read().replace('\n', '\\n')
    data2 = data2.replace('    ', '\t')


def play_view(request):
        return render(request, 'typingtest2.html', {'data2': data2})


@csrf_exempt
def multi_play_view(request):
    if request.method == 'POST':
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.set(request.user.username, request.POST['user_input'])
        opponent_data = r.get(request.POST['opponent'])
        return render(request, 'typingtest3.html',
                      {'opponent_data': opponent_data, 'data2': data2})
    else:
        return render(request, 'typingtest3.html', {'data2': data2})


@csrf_exempt
def matchmaking_view(request):
    if request.method == 'POST':
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        opponent = ''
        if r.get('host') is None:
            r.set('host', request.user.username)
            while r.get('guest') is None:
                pass
            opponent = r.get('guest')
        else:
            r.set('guest', request.user.username)
            opponent = r.get('host')
    else:
        return render(request, 'typingtest3.html', {'opponent': opponent,
                                                    'data2': data2})
