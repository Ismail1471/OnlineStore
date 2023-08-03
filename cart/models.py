from django.db import models
from pages.models import Product
from django.conf import settings

class Customer(models.Model):
    COUNTRIES_CHOICES = (
        ("us", "United States"),
        ("uk", "United Kingdom"),
        ("ger", "Germany"),
        ("fra", "France"),
        ("ind", "India"),
        ("aus", "Australia"),
        ("bra", "Brazil"),
        ("cana", "Canada"),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=50, choices=COUNTRIES_CHOICES)
    address = models.CharField(max_length=100)

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True)
    shipping = models.BooleanField(default=False)

    def get_cart_total_qty(self):
        items = self.items.all()
        total_qty = sum([item.quantity for item in items])
        return total_qty

    def get_cart_total_price(self):
        items = self.items.all()
        total_price = sum([item.get_total_price() for item in items])
        return total_price

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name="items")
    added_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)

    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

class ShippingAddress(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    town = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    comment = models.TextField()
