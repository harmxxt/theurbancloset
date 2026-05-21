from django import template

register = template.Library()

@register.filter
def get_count(counts_dict, slug):
    """Usage: {{ counts|get_count:cat.slug }}"""
    if not counts_dict:
        return 0
    return counts_dict.get(slug, 0)
