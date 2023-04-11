from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def paginate_url(value, field_name, urlencode=None):
    url = "?{}={}".format(field_name, value)
    if urlencode:
        querystring = urlencode.split("&")
        filter_querystring = filter(lambda p: p.split("=")[0] != field_name, querystring)
        encoded_querystring = "&".join(filter_querystring)
        url = "{}&{}".format(url, encoded_querystring)
        print(url)
    return url


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=2, on_ends=2):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number,
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)
