from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('about-me/', views.about_me, name='about_me_page'),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("shop/", views.shop, name="shop"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("", views.product_list, name="product_list"),
    path("contact/", views.contact_us, name="contact_us"),
    path("contact/success/", views.contact_success, name="contact_success"),
    path("product_list/", views.product_list, name="product_list"),
    path("intelligence/", views.intelligence_gathering, name="intelligence_gathering"),
    path("dns_lookup/", views.dns_lookup, name="dns_lookup"),
    path("port_scan/", views.port_scan, name="port_scan"),
    path("traceroute/", views.traceroute, name="traceroute"),
    path("web_scan/", views.web_scan, name="web_scan"),
    path("detect_os/", views.detect_os, name="detect_os"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "remove_from_cart/<int:order_item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path('multimedia/', views.multimedia, name='multimedia'),

]
