from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        models_list = models.get_models()
        for model in models_list:
            output = '{0} - {1} records'.format(model.__name__,
                                                model.objects.all().count())
            self.stdout.write(output)
            self.stderr.write('error: ' + output)
