from django.core.management.base import BaseCommand

from account.utils.location import refresh_vn_location_data


class Command(BaseCommand):
    help = "Refresh location data."

    def handle(self, *args, **options):
        refresh_vn_location_data()
