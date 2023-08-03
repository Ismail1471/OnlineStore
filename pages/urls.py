from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
        path('', views.home_view, name="home"),
        path('shop/', views.shop_view, name="shop"),
        path("shop/categories/<slug:slug>/", views.category_products, name="category_products"),
        path("shop/products/<slug:slug>", views.product_detail, name="product_detail"),
        path("shop/cart/", views.cart_view, name="cart"),
        path("checkout/", views.checkout_view, name="checkout"),
        path("payment/", views.create_checkout_session, name="payment"),
        path("payment/success/", views.success_payment, name="success_payment")
]