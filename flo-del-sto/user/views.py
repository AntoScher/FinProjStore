from django.shortcuts import render
from django.http import HttpResponseNotFound


def user_aut(request):
    return render(request, 'user/user_aut.html')

#def user_aut(request):     return HttpResponse("<h1>Это начальная страница модуля авторизации</h1>")
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
