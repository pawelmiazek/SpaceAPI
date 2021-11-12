import json
import requests
from operator import itemgetter
from itertools import chain
from django.conf import settings
from .models import Core


class _FetchCoresService:
    _CORES_QUERY = """
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

    def __init__(self, external_api_url: str):
        self._external_api_url = external_api_url

    def fetch_data(
        self,
        cores_count: int,
        exclude_unsuccessful: bool,
        exclude_upcoming: bool,
        all_cores_to_db: bool = False,
    ):
        response = requests.post(
            self._external_api_url, json={"query": self._CORES_QUERY}
        )
        if response.status_code == 200:
            data = json.loads(response.text)
            launch_cores = self.include_conditions(
                exclude_unsuccessful, exclude_upcoming, data
            )
            cores_list = self.aggregate_cores(launch_cores)
            if all_cores_to_db:
                cores_to_save = [
                    Core(
                        api_id=core[0],
                        reuse_count=core[1],
                        payload=core[2],
                    )
                    for core in cores_list
                ]
                return Core.objects.bulk_create(cores_to_save)
            cores = self.sort_cores(cores_count, cores_list)
            if len(cores) != cores_count:
                return f"There are only {len(cores)} : {cores}"
            return cores
        else:
            return "Unable to fetch data from the API."

    def include_conditions(
        self, exclude_unsuccessful: bool, exclude_upcoming: bool, data: dict
    ) -> list:
        launches = data["data"]["launches"]

        if exclude_unsuccessful:
            launches = [launch for launch in launches if launch["launch_success"]]
        if exclude_upcoming:
            launches = [launch for launch in launches if not launch["upcoming"]]

        launch_cores = []

        for item in launches:
            payload_sum = sum(
                payload_kg["payload_mass_kg"]
                for payload_kg in item["rocket"]["second_stage"]["payloads"]
                if payload_kg["payload_mass_kg"]
            )
            for core in item["rocket"]["first_stage"]["cores"]:
                if core.get("core", None):
                    launch_cores.append(
                        [
                            core["core"]["id"],
                            core["core"]["reuse_count"],
                            payload_sum * core["core"]["reuse_count"],
                        ]
                    )

        return launch_cores

    def aggregate_cores(self, data: list) -> list:
        cores_list = []

        for i, core in enumerate(data):
            if core[0] in chain(*cores_list):
                data[i][1] = data[i][1] + core[1]
                data[i][2] = data[i][2] + core[2]
            else:
                cores_list.append(core)

        return cores_list

    def sort_cores(self, cores_count: int, data: list) -> list:
        data.sort(key=itemgetter(1), reverse=True)
        cores = [tuple(c) for c in data][:cores_count]

        return cores


fetch_cores_service = _FetchCoresService(external_api_url=settings.EXTERNAL_API_URL)
