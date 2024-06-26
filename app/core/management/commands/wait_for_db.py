
# create admin command :
# https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/

from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError


class Command(BaseCommand):

    def handle(self, *args, **options):

        self.stdout.write('Waiting for database...')
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 2 sec...')
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS('Database available !'))
