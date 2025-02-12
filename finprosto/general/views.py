from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Это home страница моего итогового проекта на Django </h1>")

def flower(request):
    return HttpResponse("<h1>Это страница c каталогом цветов </h1>")
from django.shortcuts import render

# Create your views here.
