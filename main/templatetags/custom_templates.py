from django import template

register = template.Library()


@register.filter
def keyvalue(input_dict, key):
    try:
        return input_dict[key]
    except KeyError:
        return ''
