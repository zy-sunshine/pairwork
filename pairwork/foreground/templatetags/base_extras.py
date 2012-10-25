from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context = True)
def navactive(context, urls):
    request = context['request']
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""
