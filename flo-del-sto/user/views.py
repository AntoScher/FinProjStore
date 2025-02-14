from django.shortcuts import render
from django.http import HttpResponse


def user_aut(request):
    return render(request, 'user/user_aut.html')

#def user_aut(request):     return HttpResponse("<h1>Это начальная страница модуля авторизации</h1>")
#C:\DEV\GitHupRepo\FinProjStore\flo-del-sto\templates\base.html