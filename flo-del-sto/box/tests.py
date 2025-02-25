from django.test import TestCase, RequestFactory, Client
from django.urls import resolve, reverse
from users.models import User
from box import views
from general.models import Flower
from box.models import Order
from unittest.mock import patch
from django.contrib.sessions.middleware import SessionMiddleware


class BoxURLTests(TestCase):
    def test_cart_url_resolves(self):
        url = reverse('cart')
        self.assertEqual(resolve(url).func, views.cart)

    def test_add_to_cart_url_resolves(self):
        url = reverse('add_to_cart', args=[1])
        self.assertEqual(resolve(url).func, views.add_to_cart)

    def test_remove_from_cart_url_resolves(self):
        url = reverse('remove_from_cart', args=[1])
        self.assertEqual(resolve(url).func, views.remove_from_cart)

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, views.checkout)

    def test_payment_confirmation_url_resolves(self):
        url = reverse('payment_confirmation')
        self.assertEqual(resolve(url).func, views.payment_confirmation)


class CartViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.flower = Flower.objects.create(
            title="Rose",
            description="Beautiful red rose",
            price=10.99,
            slug="rose"
        )

    def test_cart_view_with_empty_cart(self):
        self.client.force_login(self.user)
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart_items', response.context)
        self.assertEqual(len(response.context['cart_items']), 0)

    def test_cart_view_with_items_in_cart(self):
        self.client.force_login(self.user)
        session = self.client.session
        session['cart'] = [self.flower.id]
        session.save()
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart_items', response.context)
        self.assertEqual(len(response.context['cart_items']), 1)
        self.assertEqual(response.context['cart_items'][0], self.flower)


class AddRemoveCartTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.flower = Flower.objects.create(
            title="Rose",
            description="Beautiful red rose",
            price=10.99,
            slug="rose"
        )

    def add_session_to_request(self, request):
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

    def test_add_to_cart(self):
        request = self.factory.get(f'/cart/add/{self.flower.id}/')
        request.user = self.user
        self.add_session_to_request(request)
        response = views.add_to_cart(request, self.flower.id)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.flower.id, request.session['cart'])

    def test_remove_from_cart(self):
        request = self.factory.get(f'/cart/remove/{self.flower.id}/')
        request.user = self.user
        self.add_session_to_request(request)
        request.session['cart'] = [self.flower.id]
        response = views.remove_from_cart(request, self.flower.id)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.flower.id, request.session['cart'])


class CheckoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.flower = Flower.objects.create(
            title="Rose",
            description="Beautiful red rose",
            price=10.99,
            slug="rose"
        )

    def test_checkout_view_get(self):
        self.client.force_login(self.user)
        session = self.client.session
        session['cart'] = [self.flower.id]
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_price', response.context)
        self.assertEqual(response.context['total_price'], self.flower.price)

    def test_checkout_view_post(self):
        self.client.force_login(self.user)
        session = self.client.session
        session['cart'] = [self.flower.id]
        session.save()
        response = self.client.post('/checkout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.client.session['cart']), 0)


class PaymentConfirmationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_payment_confirmation_view(self):
        self.client.force_login(self.user)
        response = self.client.get('/payment-confirmation/')
        self.assertEqual(response.status_code, 200)


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.flower = Flower.objects.create(
            title="Rose",
            description="Beautiful red rose",
            price=10.99,
            slug="rose"
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_price=10.99
        )
        order.flowers.add(self.flower)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.flowers.count(), 1)
        self.assertEqual(order.total_price, 10.99)
        self.assertEqual(order.status, 'pending')

    def test_order_str_method(self):
        order = Order.objects.create(
            user=self.user,
            total_price=10.99
        )
        self.assertEqual(str(order), f"Order {order.id} - {self.user.username}")


class OrderSignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.flower = Flower.objects.create(
            title="Rose",
            description="Beautiful red rose",
            price=10.99,
            slug="rose"
        )
        self.order = Order.objects.create(
            user=self.user,
            total_price=10.99
        )
        self.order.flowers.add(self.flower)

    @patch('requests.post')
    def test_notify_bot_about_status_change(self, mock_post):
        self.order.status = 'paid'
        self.order.save()
        mock_post.assert_called_once()