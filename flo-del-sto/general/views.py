from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Flower


#from .models import Flower

def index(request):
    # Добавляем переменную caption1 в контекст
    context = {
        'caption1': 'Цветочного магазина'  # Значение переменной
    }
    return render(request, 'general/index.html', context)


def flower(request, flower_id=None):
    if flower_id is None:
        flowers = Flower.objects.all()
        paginator = Paginator(flowers, 10)  # Показывать 10 на странице
        page_number = request.GET.get('page')
        flowers = paginator.get_page(page_number)
        return render(request, 'general/flowers.html', {'flowers': flowers})
    if flower_id > 2:
        return redirect('/')
    #return HttpResponse("<p>Выберите id или ктегорию цветка (slug) на странице каталога.</p>")
    #Получаем объект Flower по id
    flower = get_object_or_404(Flower, id=flower_id)
    return render(request, 'general/flower_detail.html', {'flower': flower})

def flower_slug(request,flower_slug):
   flower = get_object_or_404(Flower, slug=flower_slug)
   return render(request, 'general/flower_detail.html', {'flower': flower})

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def about(request):
    # Добавляем переменную caption1 в контекст
    context = {
        'caption1': 'Цветочного магазина'  # Значение переменной
    }
    return render(request, 'general/about.html', context)











