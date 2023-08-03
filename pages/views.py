from django.shortcuts import render, redirect
from .models import Category, MainCategory, Product, Review
from django.core.paginator import Paginator
from .forms import ReviewForm
from cart.forms import CustomerForm, ShippingAddressForm
from cart.utils import CartForAuthenticatedUser, CartForAnonymousUser
from shop import settings


def home_view(request):
    return render(request, "pages/index.html")


def shop_view(request):
    categories = Category.objects.all()
    main_categories = MainCategory.objects.all()
    products = Product.objects.all()
    sort_by = request.GET.get("sort_by")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")
    paginator = Paginator(products, 2)
    number = request.GET.get('page')
    result = paginator.get_page(number)
    if request.user.is_authenticated:
        cart = CartForAuthenticatedUser(request)
    else:
        cart = CartForAnonymousUser(request)
    if request.method == "POST":
        if request.POST.get("add"):
            slug = request.POST.get("add")
            cart.add_to_cart(slug)
    context = {
        "categories": categories,
        "main_categories": main_categories,
        "products": result,
        "sort_by": sort_by,


    }

    return render(request, "pages/shop.html", context)

def category_products(request, slug):
    main_categories = MainCategory.objects.all()
    categories = Category.objects.all()
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    sort_by = request.GET.get("sort", "l2h")
    if sort_by == "l2h":
        products = products.order_by("price")
    elif sort_by == "h2l":
        products = products.order_by("-price")
    
    context = {
        "main_categories": main_categories,
        "categories": categories,
        "products": products,
    }
    return render(request, "pages/shop.html", context)





def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    images = product.productimage_set.all()
    related_products = Product.objects.filter(category=product.category).exclude(title=product.title)
    reviews = Review.objects.filter(product=product)
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.author = request.user
        review.save()
    if request.user.is_authenticated:
        cart = CartForAuthenticatedUser(request)
    else:
        cart = CartForAnonymousUser(request)
    if request.POST.get("add"):
        cart.add_to_cart(slug=slug)
    context = {
        "form": form,
        "product": product,
        "images": images,
        "related_products": related_products,
        "reviews": reviews
    }
    return render(request, "pages/product_detail.html", context)

def cart_view(request):
    if request.user.is_authenticated:
            cart = CartForAuthenticatedUser(request)
    else:
            cart = CartForAnonymousUser(request)
    if request.method == "POST":
        if request.POST.get("delete"):
                slug = request.POST.get("delete")
                cart.delete_from_cart(slug=slug)
        if request.POST.get("clear"):
                cart.clear_cart()
    cart_info = cart.get_cart_info()
    context = {
        "items": cart_info["items"],
        "order": cart_info["order"],
        "cart_total_qty": cart_info["cart_total_quantity"],
        "cart_total_price": cart_info["cart_total_price"]
    }
    return render(request, "pages/cart.html", context)

def checkout_view(request):
    if request.user.is_authenticated:
        cart = CartForAuthenticatedUser(request)
    else:
        cart = CartForAnonymousUser(request)
    cart_info = cart.get_cart_info()
    context = {
        "ship_form": ShippingAddressForm(),
        "cus_form": CustomerForm(),
        "cart_total_qty": cart_info["cart_total_quantity"],
        "cart_total_price": cart_info["cart_total_price"]
    }
    return render(request, "pages/checkout.html", context)


def create_checkout_session(request):
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == "GET":
        if not request.user.is_authenticated:
            user_cart = CartForAnonymousUser(request)
        else:
            user_cart = CartForAuthenticatedUser(request)

        cart_info = user_cart.get_cart_info()
        total_price = cart_info["cart_total_price"]

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Товары с сайта Boutique"
                        },
                        "unit_amount": int(total_price * 100)
                    },
                    "quantity": 1
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri("payment/success/"),
            cancel_url=request.build_absolute_uri("payment/success/"),
        )

        return redirect(session.url)


def success_payment(request):
    if not request.user.is_authenticated:
        user_cart = CartForAnonymousUser(request)
    else:
        user_cart = CartForAuthenticatedUser(request)

    user_cart.clear_cart()
    return render(request, "pages/success_payment.html")






















