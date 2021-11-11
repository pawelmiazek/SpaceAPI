from django.core.management.base import BaseCommand
import json
import requests
from operator import itemgetter
from itertools import chain


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
        url = "https://api.spacex.land/graphql/"
        query = """
            {
                launches {
                    launch_success
                    upcoming
                    rocket {
                        first_stage {
                            cores {
                                core {
                                    reuse_count
                                    id
                                }
                            }
                        }
                        second_stage {
                            payloads {
                                payload_mass_kg
                            }
                        }
                    }
                }
            }
        """
        response = requests.post(url, json={"query": query})
        if response.status_code == 200:
            data = json.loads(response.text)
            launches = data["data"]["launches"]
            if options["exclude_unsuccessful"]:
                launches = [launch for launch in launches if launch["launch_success"]]
            if options["exclude_upcoming"]:
                launches = [launch for launch in launches if not launch["upcoming"]]
            launch_cores = []
            for item in launches:
                payload_sum = sum(
                    payload_kg["payload_mass_kg"]
                    for payload_kg in item["rocket"]["second_stage"]["payloads"]
                    if payload_kg["payload_mass_kg"]
                )
                for core in item["rocket"]["first_stage"]["cores"]:
                    launch_cores.append(
                        [
                            core["core"]["id"],
                            core["core"]["reuse_count"],
                            payload_sum * core["core"]["reuse_count"],
                        ]
                    )
            cores_list = []
            for i, core in enumerate(launch_cores):
                if core[0] in chain(*cores_list):
                    launch_cores[i][1] = launch_cores[i][1] + core[1]
                    launch_cores[i][2] = launch_cores[i][2] + core[2]
                else:
                    cores_list.append(core)
            cores_list.sort(key=itemgetter(1), reverse=True)
            cores = [tuple(c) for c in cores_list][: options["cores_count"]]
            if len(cores) != options["cores_count"]:
                return f"There are only {len(cores)} : {cores}"
            return f"{cores}"
        else:
            return "Unable to fetch data from the API."
