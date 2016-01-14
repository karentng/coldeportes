# encoding:utf-8
from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context
from entidades.views import refresh_public

class Command(BaseCommand):
    def handle(self, *args, **options):
        from coldeportes.utilities import refresh_public
        refresh_public()