from django import template

register = template.Library()


@register.filter
def times(num: int | float):
    """Gives a range of numbers from 0 to num-1."""
    return range(int(num))


@register.filter
def has_decimal_greater_than_0(num: float):
    """Checks if the decimal part of a number is greater than 0."""
    return num % 1 > 0

@register.filter
def order_by(queryset, field):
    """Orders a queryset by a given field."""
    return queryset.order_by(field)

@register.filter
def not_in(value, valid_list):
    return value not in [v.strip() for v in valid_list.split(",")]

@register.simple_tag(takes_context=True)
def querystring_without(context, *keys_to_exclude):
    query = context['request'].GET.copy()
    for key in keys_to_exclude:
        query.pop(key, None)
    return query.urlencode()
