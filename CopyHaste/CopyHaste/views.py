from django.shortcuts import render


def home_view(request):
    return render(request, 'typingtest2.html')