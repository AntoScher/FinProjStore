from django.contrib import admin
from .models import Flower

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'slug')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
