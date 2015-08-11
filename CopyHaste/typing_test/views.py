from django.shortcuts import render

with open("typing_test/test1.txt", "r") as myfile:
    data2 = myfile.read().replace('\n', '\\n')
    data2 = data2.replace('    ', '\t')


def play_view(request):
    return render(request, 'typingtest2.html', {'data2': data2})
