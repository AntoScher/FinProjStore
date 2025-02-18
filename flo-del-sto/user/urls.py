from django.urls import path
from . import views

urlpatterns = [
path('user_aut/', views.user_aut, name='autor'),

]