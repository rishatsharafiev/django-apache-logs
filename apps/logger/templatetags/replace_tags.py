from django import template
register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """Query parameter replace"""
    d = request.GET.copy()
    d[field] = value
    return d.urlencode()


@register.simple_tag
def url_delete(request, field):
    """Query parameter delete"""
    d = request.GET.copy()
    del d[field]
    return d.urlencode()
