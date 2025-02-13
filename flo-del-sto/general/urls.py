from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('flower/<int:flower_id>', views.flower, name='flower_id'),
    path('flower/<slug:flower_slug>/', views.flower_slug, name='flower_slug'),
]