import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'home.html' in [t.name for t in response.templates]

def test_portfolio_view(client):
    response = client.get(reverse('portfolio'))
    assert response.status_code == 200
    assert 'portfolio.html' in [t.name for t in response.templates]

def test_shop_view(client):
    response = client.get(reverse('shop'))
    assert response.status_code == 200
    assert 'shop.html' in [t.name for t in response.templates]

def test_register_view_get(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200
    assert 'register.html' in [t.name for t in response.templates]

def test_register_view_post(client, db):
    response = client.post(reverse('register'), {
        'username': 'newuser',
        'password1': 'newpassword',
        'password2': 'newpassword'
    })
    assert response.status_code == 302  # Redirects to login after successful registration

def test_login_view_get(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'login.html' in [t.name for t in response.templates]

def test_login_view_post(client, user):
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Redirects to home after successful login

def test_logout_view(client, user):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('logout'))
    assert response.status_code == 302  # Redirects to home after logout

def test_cart_view(client, user):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert 'cart.html' in [t.name for t in response.templates]

def test_add_to_cart_view(client, user, product):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('add_to_cart', args=[product.id]))
    assert response.status_code == 302  # Redirects to cart after adding to cart

def test_checkout_view(client, user):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('checkout'))
    assert response.status_code == 200
    assert 'checkout.html' in [t.name for t in response.templates]

def test_remove_from_cart_view(client, user, order_item):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('remove_from_cart', args=[order_item.id]))
    assert response.status_code == 302  # Redirects to cart after removing from cart

def test_contact_us_view_get(client):
    response = client.get(reverse('contact_us'))
    assert response.status_code == 200
    assert 'contact.html' in [t.name for t in response.templates]

def test_contact_us_view_post(client):
    response = client.post(reverse('contact_us'), {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'message': 'This is a test message.'
    })
    assert response.status_code == 302  # Redirects to contact_success after sending message

def test_contact_success_view(client):
    response = client.get(reverse('contact_success'))
    assert response.status_code == 200
    assert 'success.html' in [t.name for t in response.templates]

def test_intelligence_gathering_view_get(client, user):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('intelligence_gathering'))
    assert response.status_code == 200
    assert 'intelligence_gathering.html' in [t.name for t in response.templates]

def test_intelligence_gathering_view_post(client, user):
    client.login(username='testuser', password='testpassword')
    response = client.post(reverse('intelligence_gathering'), {
        'target': 'example.com',
        'intelligence_option': 'port_scan'
    })
    assert response.status_code == 200
    assert 'intelligence_gathering.html' in [t.name for t in response.templates]
