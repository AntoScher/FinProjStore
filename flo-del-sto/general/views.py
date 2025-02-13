from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
import re


def index(request):
    return HttpResponse("<h1>Это home страница моего итогового проекта на Django </h1>")

def flower(request,flower_id):
    if flower_id>2:
        return redirect('/')
    return HttpResponse(f"<h1>Это страница c каталогом цветов </h1><p>id: {flower_id}</p>")

def flower_slug(request,flower_slug):
    # Регулярное выражение для проверки slug
    valid_slug_pattern =  r'^[a-zA-Z0-9_-]+$'

    # Проверяем, соответствует ли flower_slug регулярному выражению
    if not re.match(valid_slug_pattern, flower_slug):
     return redirect('/')

    return HttpResponse(f"<h1>Это страница c каталогом цветов </h1><p>slug: {flower_slug}</p>")



def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")



"""  эта хренъ почему то не работает в if 
    # Если slug не совпадает, возвращаем сообщение об ошибке
          return HttpResponse(
            "<h1>Проверьте адрес страницы</h1>"
            "<p>slug: {}</p>".format(flower_slug)) """