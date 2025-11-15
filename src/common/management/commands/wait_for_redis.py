import time
from urllib.parse import urlparse

import redis
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Wait for Redis to be ready before continuing.'

    def add_arguments(self, parser):
        parser.add_argument('--max-retries', type=int, default=30)
        parser.add_argument('--delay', type=float, default=1.0)
        parser.add_argument('--url', type=str, default=settings.CACHES['default']['LOCATION'])

    def handle(self, *args, **options):
        url = options['url']
        parsed = urlparse(url)
        display = f'{parsed.hostname}:{parsed.port or 6379}'

        self.stdout.write(f'Waiting for Redis at {display}...')
        retries = 0

        while True:
            try:
                redis.from_url(url, socket_connect_timeout=1).ping()
                break
            except redis.ConnectionError as exc:
                retries += 1
                if retries > options['max_retries']:
                    self.stderr.write(
                        self.style.ERROR(f'Redis not available after {options["max_retries"]} retries')
                    )
                    raise SystemExit(1) from exc
                self.stdout.write(f'Redis unavailable, retry {retries}/{options["max_retries"]}...')
                time.sleep(options['delay'])

        self.stdout.write(self.style.SUCCESS(f'Redis available at {display}!'))
