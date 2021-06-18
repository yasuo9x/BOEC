from django import template
register = template.Library()

@register.filter
def list_item(lst, i):
    return lst[i]


@register.filter
def mul(item1,item2):
    item1 = int(item1)
    item2 =int(item2)
    return item1 * item2 