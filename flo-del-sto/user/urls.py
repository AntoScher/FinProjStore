from django.urls import path
from . import views

urlpatterns = [
path('', views.user_aut, name='autor'),

path('user_aut/', views.user_aut, name='autor'),
#path('user_aut/', views.user_aut, name='user_aut'),
]