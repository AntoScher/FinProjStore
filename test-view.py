from django.shortcuts import render
from .models import Flower  # Импортируйте модель Flower, если она существует

def flower(request, flower_id=None):
    if flower_id is None:
        flowers = Flower.objects.all()  # Получите все цветы из базы данных
        return render(request, 'general/flowers.html', {'flowers': flowers})
    if flower_id > 2:
        return redirect('/')
    return HttpResponse("<p>Выберите №(id) цветка или его обозначение (slug) для получения дополнительной информации.</p>")