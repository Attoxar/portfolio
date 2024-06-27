import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from webside.main.models import Product, Order, OrderItem
from django.core import mail
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'webside.webside.settings'

django.setup()


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10.00)
        self.contact_url = reverse('contact_us')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_portfolio_view(self):
        response = self.client.get(reverse('portfolio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio.html')

    def test_shop_view(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['products']), 1)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout_view'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_cart_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(OrderItem.objects.filter(product=self.product, order__user=self.user).count(), 1)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.create(user=self.user, ordered=False)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=1, ordered=False)
        response = self.client.get(reverse('remove_from_cart', args=[order_item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(OrderItem.objects.filter(id=order_item.id).count(), 0)

    def test_checkout_view(self):
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.create(user=self.user, ordered=False)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, ordered=False)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')
        self.assertIn('total_price', response.context)
        self.assertEqual(response.context['total_price'], self.product.price)

    def test_contact_us_view(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

        response = self.client.post(self.contact_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'message': 'Hello!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'testuser')
        self.assertEqual(mail.outbox[0].body, 'Hello!')
        self.assertEqual(mail.outbox[0].from_email, 'test@example.com')
        self.assertEqual(mail.outbox[0].to, ['andreas.blanck@ymail.com'])
