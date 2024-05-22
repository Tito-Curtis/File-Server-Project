import os
from django import template


register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value)

@register.filter
def extension(value):
    return os.path.splitext(value)[1]