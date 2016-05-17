from django import template
register = template.Library()


@register.filter(name='can_manage')
def can_manage(id_tenant):
    """
    Autor: Juan Diego García
    Abril 4 2016
    template tag filter para verificar si el tenant del request pertenece a alguno de los incluidos en el arreglo
    :param id_tenant: id del tipo del tenant correspondiente
    :return:
    """
    return id_tenant in (3, 11)
