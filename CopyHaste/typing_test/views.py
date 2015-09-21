from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from cnh_scores.models import Matches, UserScores
import redis
import urllib2
import re
import json
from random import randint


with open("typing_test/test1.txt", "r") as myfile:
    data2 = myfile.read().replace('\n', '\\n')
    data2 = data2.replace('    ', '\t')


def play_view(request):
    return render(request, 'typingtest2.html', {'data2': data2})


@csrf_exempt
def multi_play_view(request, opponent=None):
    if request.method == 'POST':
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.set(request.user.username, request.POST['user_input'])
        opponent_data = r.get(request.POST['opponent'])
        return HttpResponse(opponent_data)


@csrf_exempt
def matchmaking_view(request):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    opponent = ''
    if r.get('host') is None:
        role = 'host'
        r.set('host', request.user.username)
        while r.get('guest') is None:
            pass
        opponent = r.get('guest')
        r.delete('guest')
    else:
        role = 'guest'
        r.set('guest', request.user.username)
        opponent = r.get('host')
        r.delete('host')
        r.set(request.user.username, '')
    return render(request, 'typingtest3.html',
                  {'opponent': opponent, 'role': role})


def get_code(language):
    while True:
        # Get the 100 most recently updated repos that are large and pick one randomly.
        url = ('https://api.github.com/search/repositories?q=language:' +
               '{}+sort:updated+size:>20000&per_page=100'.format(language))
        data = json.load(urllib2.urlopen(url))
        try:
            info = data['items'][randint(0, 99)]
        except:
            continue
        repo = info['name']
        user = info['owner']['login']
        full_name = info['full_name']

        # Get the files and pick one randomly.
        repo_url = ('https://api.github.com/search/code?q=language:' +
                    '{}+sort:size+repo:{}'.format(language, full_name))
        data = json.load(urllib2.urlopen(repo_url))
        try:
            path = data['items'][randint(0, len(data['items'])-1)]['path']
        except:
            continue
        print path
        # Get the raw text of the file.
        code = urllib2.urlopen("https://raw.githubusercontent.com/{}/{}/master/{}"
                               .format(user, repo, path)).read()
        print code
        # Get rid of doc strings, comments, import statements, blank lines and
        # convert multi spaces to tabs.

        code = re.sub(r'[\s]*"{3}([\s\S]*?"{3})', '', code)
        code = re.sub(r"[\s]*'{3}([\s\S]*?'{3})", '', code)
        code = re.sub(r'[\s]*#([\w\W\s].*)', '', code)
        code = re.sub(r'[\s]*from([\w\W\s].*)', '', code)
        code = re.sub(r'[\s]*import([\w\W\s].*)', '', code)
        code = re.sub(r'^[\s]*$', '', code)
        code = re.sub(r'\n{2,}', '\n', code)
        code = re.sub(r'[ ]{4}', '\t', code)
        code = code.lstrip()
        if len(code) > 750:
            return code


@csrf_exempt
def get_content_view(request):
    print 1
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    print request.POST
    if request.POST['role'] == 'guest':
        print 2.1
        while r.get(request.POST['opponent'] + "_sample") is None:
            pass
        code = r.get(request.POST['opponent'] + "_sample")
        r.delete(request.POST['opponent'] + "_sample")

        return HttpResponse(code)

    if request.POST['role'] == 'host':
        print 3.1
        user = request.POST['user']
        repo = request.POST['repo']
        path = request.POST['path']
        code = urllib2.urlopen("https://raw.githubusercontent.com/{}/{}/master/{}"
                               .format(user, repo, path)).read()
        code = str(code)
        code = re.sub(r'"""([\w\W\s]+)"""', '', code)
        code = re.sub(r'#([\w\W\s].*)', '', code)
        code = re.sub(r'from([\w\W\s].*)', '', code)
        code = re.sub(r'import([\w\W\s].*)', '', code)
        code = code.lstrip()
        r.set(request.user.username + "_sample", code)
        return HttpResponse(code)


@csrf_exempt
def get_content_view2(request):
    return HttpResponse(get_code('python'))


@csrf_exempt
def report_results_view(request):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set(request.user.username + 'wpm_net', request.POST['wpm_net'])
    r.set(request.user.username + 'wpm_gross', request.POST['wpm_gross'])
    r.set(request.user.username + 'mistakes', request.POST['mistakes'])
    if r.get(request.POST['opponent'] + 'wpm_net') is None:
        return HttpResponse("nope")
    while r.get(request.POST['opponent'] + 'wpm_net') is None:
        pass
    user1 = UserScores()
    user1.user = request.user
    user1.wpm_gross = request.POST['wpm_gross']
    user1.wpm_net = request.POST['wpm_net']
    user1.mistakes = request.POST['mistakes']
    user1.save()
    user2 = UserScores()
    user2.user = User.objects.get(username=request.POST['opponent'])
    user2.wpm_gross = r.get(request.user.username + 'wpm_gross')
    user2.wpm_net = r.get(request.user.username + 'wpm_net')
    user2.mistakes = r.get(request.user.username + 'mistakes')
    user2.save()
    winner = ''
    loser = ''
    if user1.wpm_net > user2.wpm_net:
        winner = user1
        loser = user2
    else:
        winner = user2
        loser = user1
    match = Matches()
    match.winner = winner
    match.loser = loser
    match.save()
    r.delete(request.user.username + 'wpm_gross')
    r.delete(request.user.username + 'wpm_net')
    r.delete(request.user.username + 'mistakes')
    r.delete(request.user.username)
    r.delete(request.POST['opponent'] + 'wpm_gross')
    r.delete(request.POST['opponent'] + 'wpm_net')
    r.delete(request.POST['opponent'] + 'mistakes')
    r.delete(request.POST['opponent'])
    return HttpResponse("nope")
