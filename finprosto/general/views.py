from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Это home страница моего итогового проекта на Django </h1>")


from django.shortcuts import render

# Create your views here.
