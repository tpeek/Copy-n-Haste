from django.shortcuts import render

with open("CopyHaste/test1.txt", "r") as myfile:
    data1 = myfile.read().replace('\n', '')

with open("CopyHaste/test1.txt", "r") as myfile:
    data2 = myfile.read()


def home_view(request):
    return render(request, 'typingtest2.html', {'data2': data2})


def auth_view(request):
    return
