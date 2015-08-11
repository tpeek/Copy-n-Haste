from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


def auth_view(request):
    return
