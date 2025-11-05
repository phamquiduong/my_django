import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Wait for database to be ready before continuing.'

    def add_arguments(self, parser):
        parser.add_argument('--max-retries', type=int, default=30)
        parser.add_argument('--delay', type=float, default=1.0)
        parser.add_argument('--db', type=str, default='default')

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        retries = 0
        db_name = options['db']
        while True:
            try:
                conn = connections[db_name]
                conn.cursor()
                break
            except OperationalError as exc:
                retries += 1
                if retries > options['max_retries']:
                    self.stderr.write(
                        self.style.ERROR(f"Database '{db_name}' not available after {options['max_retries']} retries")
                    )
                    raise SystemExit(1) from exc
                self.stdout.write(f"Database '{db_name}' unavailable, retry {retries}/{options['max_retries']}...")
                time.sleep(options['delay'])
        self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' available!"))
