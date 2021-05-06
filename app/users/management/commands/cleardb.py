# used during container startup to clear default db data before importing from json dump file

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        qs = ContentType.objects.all()
        count = qs.count()
        qs.delete()
        self.stdout.write(f"Cleared {count} db entries\n")
