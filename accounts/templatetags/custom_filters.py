# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='pop_price')
def pop_price(prices_list):
    try:
        return prices_list.pop(0)
    except IndexError:
        return None