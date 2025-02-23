from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests
from general.models import Flower  # Импортируем модель Flower

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flowers = models.ManyToManyField(Flower)  # Изменяем поле на flowers и используем модель Flower
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    # Сохраняем предыдущее значение статуса
    _status_before_update = None

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Получаем старое значение статуса
            old_instance = Order.objects.get(pk=self.pk)
            self._status_before_update = old_instance.status
        super().save(*args, **kwargs)


@receiver(post_save, sender=Order)
def notify_bot_about_status_change(sender, instance, **kwargs):
    """Отправляет уведомление боту при изменении статуса заказа."""
    # Проверяем, изменился ли статус
    if instance._status_before_update != instance.status:
        data = {
            'telegram_id': 1367180406,  # ID пользователя из Telegram
            'order_id': instance.id,
            'new_status': instance.status,
            'total_price': float(instance.total_price),
        }
        try:
            # Отправка POST-запроса к вашему боту
            response = requests.post('http://127.0.0.1:8080/notify/', json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            # Логируем ошибки
            print(f"Ошибка при отправке уведомления: {e}")
