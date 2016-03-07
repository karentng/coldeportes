from django import template
from django.contrib.auth.models import Group
register = template.Library()
@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Autor: Milton Lenis
    Marzo 4 2016
    template tag filter para verificar si un usuario pertenece a un grupo
    :param user:
    :param group_name:
    :return:
    """
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
