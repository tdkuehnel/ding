import os
import uuid
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(name='cache_bust')
def cache_bust():
    if settings.DEBUG:
        version = uuid.uuid1()
    else:
        version = os.environ.get('PROJECT_VERSION')
        if version is None:
            version = '1'

    return '__v__={version}'.format(version=version)

@register.filter
def duration(td):

    string = td.__str__().replace('days', 'Tage').replace('day','Tag')
    string = string[:string.find('.')]
    return string

@register.filter
def ohnepunkt(objekt):
    text = objekt.__str__()
    if text.endswith('.'):
        text = text[:-1]
    return text

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def satzklein(satz):
    return satz[0].lower() + satz[1:]
