from django.shortcuts import render

with open("CopyHaste/test1.txt", "r") as myfile:
    data1 = myfile.read().replace('\n', '')

with open("CopyHaste/test1.txt", "r") as myfile:
    data2 = myfile.read().replace('\n', '\\n')
    data2 = data2.replace('    ', '\t')


def home_view(request):
    if request.method == 'POST':
        print request.POST['wpm_net']
        print request.POST['wpm_gross']
        print request.POST['errors']
        print request.POST['score']
    return render(request, 'typingtest2.html', {'data2': data2})


def auth_view(request):
    return
