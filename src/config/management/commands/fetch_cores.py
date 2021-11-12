from django.core.management.base import BaseCommand
import json
import requests
from operator import itemgetter
from itertools import chain
from cores.services import fetch_cores_service


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "cores_count", type=int, help="Number of most reused rocket cores to fetch"
        )
        parser.add_argument(
            "exclude_unsuccessful",
            type=bool,
            help="Exclude or exclude unsuccessful flights",
        )
        parser.add_argument(
            "exclude_upcoming",
            type=bool,
            help="Exclude or exclude planned future missions",
        )

    def handle(self, *args, **options):
        cores = fetch_cores_service.fetch_data(
            options["cores_count"],
            options["exclude_unsuccessful"],
            options["exclude_upcoming"],
        )
        return f"{cores}"
