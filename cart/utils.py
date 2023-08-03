from .models import Order, OrderProduct
from pages.models import Product
from shop import settings


class CartForAuthenticatedUser:
    def __init__(self, request):
        self.customer = request.user
        self.order, created = Order.objects.get_or_create(customer=self.customer)
        self.items = self.order.items.all()


    def add_to_cart(self, slug):
        product = Product.objects.get(slug=slug)
        item, created = OrderProduct.objects.get_or_create(
            cart=self.order,
            product=product

        )
        if not created:
            item.quantity += 1
            item.save()

    def delete_from_cart(self, slug):
        product = Product.objects.get(slug=slug)
        item, created = OrderProduct.objects.get_or_create(cart=self.order, product=product)
        if item.quantity == 1:
            item.delete()
        else:
            item.quantity -= 1
            item.save()

    def clear_cart(self):
        for item in self.items:
            item.delete()

    def get_cart_info(self):
        return {
            "order": self.order,
            "items": self.items,
            "cart_total_quantity": self.order.get_cart_total_qty(),
            "cart_total_price": self.order.get_cart_total_price(),
        }

class CartForAnonymousUser:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.get_cart()


    def get_cart(self):
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session["cart"] = {}
        return cart

    def add_to_cart(self, slug):
        key = slug
        cart_product = self.cart.get(key)
        if cart_product:
            cart_product["quantity"] += 1
        else:
            self.cart[key] = {"quantity": 1
                              }
        self.save()

    def delete_from_cart(self, slug):
        key = slug
        cart_product = self.cart.get(key)
        if cart_product["quantity"] == 1:
            self.cart.pop(key)
        else:
            cart_product["quantity"] -= 1
        self.save()

    def clear_cart(self):
        self.cart.clear()


    def get_cart_info(self):
        products = []
        order = {
            "get_cart_total_price": 0,
            "get_cart_total_quantity": 0,
        }
        cart_total_quantity = order["get_cart_total_quantity"]
        cart_total_price = order["get_cart_total_price"]
        for key in self.cart:
            if self.cart[key]["quantity"] > 0:
                product_quantity = self.cart[key]["quantity"]
                cart_total_quantity += product_quantity
                product = Product.objects.get(slug=key)
                get_total_price = product.price * product_quantity

                cart_product = {
                    "pk": product.pk,
                    "product": {
                        "slug": product.slug,
                        "title": product.title,
                        "price": product.price,
                        "get_first_photo": product.get_first_photo(),
                        "quantity": product.quantity,
                        "get_absolute_url": product.get_absolute_url()
                    },
                    "quantity": product_quantity,
                    "get_total_price": get_total_price
                }

                products.append(cart_product)
                order["get_cart_total_price"] += cart_product["get_total_price"]
                order["get_cart_total_quantity"] += cart_product["quantity"]
                cart_total_price = order["get_cart_total_price"]

        self.save()


        return {
            "cart_total_quantity": cart_total_quantity,
            "cart_total_price": cart_total_price,
            "order": order,
            "items": products
        }

    def save(self):
        self.session.modified = True












