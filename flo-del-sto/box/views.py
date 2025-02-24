from django.shortcuts import render, redirect
from .models import Order
from general.models import Flower
from django.contrib.auth.decorators import login_required
from decimal import Decimal

def cart_view(request):
    # Логика для обработки корзины
    return render(request, 'cart.html')

@login_required
def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart_items = Flower.objects.filter(id__in=request.session['cart'])
    total_price = sum(flower.price for flower in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, flower_id):
    if 'cart' not in request.session:
        request.session['cart'] = []
    if flower_id not in request.session['cart']:
        request.session['cart'].append(flower_id)
        request.session.modified = True
    return redirect('cart')

@login_required
def remove_from_cart(request, flower_id):
    if 'cart' in request.session:
        request.session['cart'] = [item for item in request.session['cart'] if item != flower_id]
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
        # Добавляем цветы из корзины в заказ
        cart_items = Flower.objects.filter(id__in=request.session.get('cart', []))
        for flower in cart_items:
            order.flowers.add(flower)
            order.total_price += flower.price
        order.save()
        # Очищаем корзину
        request.session['cart'] = []
        # Перенаправляем на страницу подтверждения оплаты
        return redirect('payment_confirmation')

    # Если метод GET, просто отображаем страницу оформления заказа
    cart_items = Flower.objects.filter(id__in=request.session.get('cart', []))
    total_price = sum(flower.price for flower in cart_items)
    return render(request, 'checkout.html', {'total_price': total_price})

@login_required
def payment_confirmation(request):
    return render(request, 'payment_confirmation.html')