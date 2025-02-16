from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
import re
#from .models import Flower

def index(request):
    # Добавляем переменную caption1 в контекст
    context = {
        'caption1': 'FlowerShop'  # Значение переменной
    }
    return render(request, 'general/index.html', context)

def flower(request,flower_id=None):
 #   №def flower(request,flower_id=None):
    if flower_id is None:
        flowers = Flower.objects.all()
        return render(request, 'general/flowers.html', {'flowers': flowers})
    if flower_id>2:
        return redirect('/')
    return HttpResponse("<p>Выберите №(id) цветка или его обозначение (slug) для получения дополнительной информации.</p>")
    flower = get_object_or_404(Flower, id=flower_id)
    return render(request, 'general/flower_detail.html', {'flower': flower})

def flower_slug(request,flower_slug):
    # Регулярное выражение для проверки slug
    valid_slug_pattern =  r'^[a-zA-Z0-9_-]+$'
    # Проверяем, соответствует ли flower_slug регулярному выражению
    if not re.match(valid_slug_pattern, flower_slug):
        return redirect('/')
    flower = get_object_or_404(Flower, slug=flower_slug)
    return render(request, 'general/flower_detail.html', {'flower': flower})
#return render(request, 'general/flowers.html')
#return HttpResponse(f"<h1>Это страница c каталогом цветов </h1><p>slug: {flower_slug}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
from django.shortcuts import render, get_object_or_404
from .models import Flower

