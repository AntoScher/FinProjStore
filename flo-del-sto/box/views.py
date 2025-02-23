from django.shortcuts import render, redirect
from .models import  Order
from general.models import Flower
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
def cart_view(request):
    # Логика для обработки корзины
    return render(request, 'cart.html')

@login_required
def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart_items = Flower.objects.filter(id__in=request.session['cart'])
    total_price = sum(car.price for car in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



@login_required
def add_to_cart(request, car_id):
    if 'cart' not in request.session:
        request.session['cart'] = []
    if car_id not in request.session['cart']:
        request.session['cart'].append(car_id)
        request.session.modified = True
    return redirect('cart')


@login_required
def remove_from_cart(request, car_id):
    if 'cart' in request.session:
        request.session['cart'] = [item for item in request.session['cart'] if item != car_id]
        request.session.modified = True
    return redirect('cart')


@login_required
def checkout(request):
    if request.method == 'POST':
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            total_price=Decimal('0.00')  # Заглушка, пока не считаем общую стоимость
        )
        # Добавляем машины из корзины в заказ
        cart_items = Car.objects.filter(id__in=request.session.get('cart', []))
        for car in cart_items:
            order.cars.add(car)
            order.total_price += car.price
        order.save()
        # Очищаем корзину
        request.session['cart'] = []
        # Перенаправляем на страницу подтверждения оплаты
        return redirect('payment_confirmation')

    # Если метод GET, просто отображаем страницу оформления заказа
    cart_items = Car.objects.filter(id__in=request.session.get('cart', []))
    total_price = sum(car.price for car in cart_items)
    return render(request, 'checkout.html', {'total_price': total_price})


@login_required
def payment_confirmation(request):
    return render(request, 'payment_confirmation.html')
