from django import template

register = template.Library()

@register.filter
def attr(obj, name):
    """Return attribute of object by string name, or key if dict."""
    if isinstance(obj, dict):
        return obj.get(name, '')
    return getattr(obj, name, '')
