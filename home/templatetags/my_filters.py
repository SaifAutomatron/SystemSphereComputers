from django.template.library import Library

register = Library()


@register.filter(name='times')
def times(number):
    return range(number)
