from django import template

from ..models import Order

register = template.Library()

@register.simple_tag()
def get_order(request):
    customer = request.user
    order = Order.objects.get(customer=customer)
    return order