from django.urls import path
from . import views

urlpatterns = [
path('user_aut/', views.user_aut, name='autor'),
path('register/', views.register, name='register'),
path('password_reset/', views.password_reset, name='password_reset'),
#path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),

]
