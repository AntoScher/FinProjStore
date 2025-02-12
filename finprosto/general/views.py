from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect

def index(request):
    return HttpResponse("<h1>Это home страница моего итогового проекта на Django </h1>")

def flower(request,flower_id):
    if flower_id>2:
        return redirect('/')
    return HttpResponse(f"<h1>Это страница c каталогом цветов </h1><p>id: {flower_id}</p>")

def flower_slug(request,flower_slug):
    return HttpResponse(f"<h1>Это страница c каталогом цветов </h1><p>slug: {flower_slug}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
# Create your views here.
#def categories(request, cat_id):    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")
#def categories_by_slug(request, cat_slug): return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")
