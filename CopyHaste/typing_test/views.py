from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import urllib

with open("typing_test/test1.txt", "r") as myfile:
    data2 = myfile.read().replace('\n', '\\n')
    data2 = data2.replace('    ', '\t')


def play_view(request):
        return render(request, 'typingtest2.html', {'data2': data2})


@csrf_exempt
def multi_play_view(request):
    if request.method == 'POST':
        print request.POST['user_input']
        return render(request, 'typingtest3.html', {'data2': data2})
    return render(request, 'typingtest3.html', {'data2': data2})


@csrf_exempt
def get_content_view(request):
    user = request.POST['user']
    repo = request.POST['repo']
    path = request.POST['path']
    print user, repo, path
    code = urllib.urlopen("https://raw.githubusercontent.com/{}/{}/master/{}".format(user, repo, path)).read()
    code = str(code)
    return HttpResponse(code)
