from django import template

register = template.Library()

@register.filter
def is_string(value):
    return isinstance(value, str)

@register.filter
def to_string(value):
    return str(value)



