from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
path('cart/', views.cart_view, name='cart'),
path('cart/add/<int:car_id>/', views.add_to_cart, name='add_to_cart'),
path('cart/remove/<int:car_id>/', views.remove_from_cart, name='remove_from_cart'),
path('checkout/', views.checkout, name='checkout'),
path('payment-confirmation/', views.payment_confirmation, name='payment_confirmation'),
]
