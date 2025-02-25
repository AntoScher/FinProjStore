import os
import django
from django.test import TestCase
from general.models import Flower

# Указываем Django, какие настройки использовать
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flo-del-sto.settings")

# Инициализируем Django
django.setup()

class FlowerModelTest(TestCase):
    def setUp(self):
        # Очищаем все объекты Flower перед каждым тестом
        Flower.objects.all().delete()

    def test_flower_creation(self):
        flower = Flower.objects.create(
            title="Rose",
            description="Beautiful red rose",
            price=10.99,
            slug="rose"
        )
        self.assertEqual(flower.title, "Rose")
        self.assertEqual(flower.description, "Beautiful red rose")
        self.assertEqual(flower.price, 10.99)
        self.assertEqual(flower.slug, "rose")
        self.assertTrue(flower.id)

    def test_flower_unique_slug(self):
        # Создаем первый объект
        Flower.objects.create(
            title="Rose",
            description="Beautiful red rose",
            price=10.99,
            slug="rose"
        )
        # Пытаемся создать второй объект с тем же slug
        with self.assertRaises(Exception):
            Flower.objects.create(
                title="Tulip",
                description="Yellow tulip",
                price=5.99,
                slug="rose"  # Дубликат slug
            )