"""Small UI helpers, compatible with the current and target Django versions."""
from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag(takes_context=True)
def page_query(context, page):
    request = context.get('request')
    params = request.GET.copy() if request is not None else QueryDict('', mutable=True)
    params['page'] = str(page)
    return '?' + params.urlencode()
