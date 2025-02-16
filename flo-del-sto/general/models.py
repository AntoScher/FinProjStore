from django.db import models

class Flower(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='flowers/', verbose_name="Изображение")
    slug = models.SlugField(unique=True, verbose_name="Категория")

    def __str__(self):
        return self.title

    """
    Модель данных:
    - Таблица
    пользователей(ID, имя, email, телефон, адрес).
    - Таблица
    товаров(ID, название, цена, изображение).
    - Таблица
    заказов(ID, пользователь, товары, статус, дата
    заказа).
    - Таблица
    отзывов(ID, пользователь, товар, отзыв, рейтинг).
    - Таблица
    отчетов(ID, дата, заказ, данные
    по
    продажам, прибыль, расходы).
    """