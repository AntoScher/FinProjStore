from django.urls import path
from . import views

urlpatterns = [
path('', views.user_aut, name='autor'),
	#path('user/', views.user_aut, name='autor'),

]