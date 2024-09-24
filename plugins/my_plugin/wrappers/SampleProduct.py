import json
import random
from uuid import uuid4
from pathlib import Path

import requests
import requests_mock

from plugins.my_plugin.wrappers.CommonProtocol import CommonProtocol


RESOURCES_DIR = Path(__file__).parents[1].joinpath("samples")


class SampleProduct(CommonProtocol):
    def __init__(self, root_url):
        self.service_url = root_url
        with open(RESOURCES_DIR.joinpath("servers.json")) as servers_src, open(
            RESOURCES_DIR.joinpath("os.json")
        ) as os_src, open(RESOURCES_DIR.joinpath("drives.json")) as drives_src:
            self.available_servers = json.load(servers_src)
            self.available_os = json.load(os_src)
            self.available_drives = json.load(drives_src)

    def create_new_admin_user_session(self, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(
                f"{self.service_url}/users/create_admin",
                json={
                    "response": {
                        "user_id": str(uuid4()),
                        "token": str(uuid4()),
                        "user_data": {
                            "username": "sample_admin",
                            "role": "admin",
                        },
                    }
                },
            )
            return requests.post(f"{self.service_url}/users/create_admin").json()

    def get_resources(self, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.get(
                f"{self.service_url}/resources",
                json={
                    "servers": self.available_servers,
                    "os": self.available_os,
                    "drives": self.available_drives,
                },
            )
            return requests.get(f"{self.service_url}/resources").json()

    def reserve_resource(self, resource_config, user_data, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(
                f"{self.service_url}/reserve/{resource_config['server']['model']}",
                json={
                    "reservation_id": str(uuid4()),
                    "reserver_id": user_data["user_id"],
                },
            )
            return requests.post(
                f"{self.service_url}/reserve/{resource_config['server']['model']}"
            )

    def wait_deploy(self, reservation_id, reserver_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.get(
                f"{self.service_url}/deploy/{reservation_id}/{reserver_id}",
                json={"reservation_status": random.randint(0, 1)},
            )
            response = requests.get(
                f"{self.service_url}/deploy/{reservation_id}/{reserver_id}"
            ).json()
            while not response["reservation_status"]:
                mock_request.get(
                    f"{self.service_url}/deploy/{reservation_id}/{reserver_id}",
                    json={"reservation_status": random.randint(0, 1)},
                )
                response = requests.get(
                    f"{self.service_url}/deploy/{reservation_id}/{reserver_id}"
                ).json()
            return response

    def release_resource(self, reservation_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(
                f"{self.service_url}/reserve/{reservation_id}",
                json={
                    "released": reservation_id,
                    "by_user": kwargs.get("user_data", {})["user_id"],
                },
            )
            return requests.post(f"{self.service_url}/reserve/{reservation_id}")

    def get_available_os(self, *args, **kwargs):
        if kwargs.get("filter"):
            print([filter_field for filter_field in kwargs["filter"]])
            return next(
                av_os
                for av_os in self.available_os
                if all(
                    av_os[filter_field] == kwargs["filter"][filter_field]
                    for filter_field in kwargs["filter"]
                )
            )

    def install_os(self, resource_config, reservation_id, target_os, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(
                f"{self.service_url}/deploy_os/{reservation_id}",
                json={
                    "details": {
                        "reservation_id": reservation_id,
                        "resource": resource_config,
                        "target_os": target_os,
                        "installation_status": "pending",
                    }
                },
            )
            return requests.post(
                f"{self.service_url}/deploy_os/{reservation_id}",
                json=resource_config,
            ).json()

    def get_os_installation_status(self, reservation_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.get(
                f"{self.service_url}/deploy_os/{reservation_id}",
                json={
                    "reservation_id": reservation_id,
                    "installation_status": random.choice(
                        ["processing", "complete", "failed"]
                    ),
                },
            )
            return requests.get(f"{self.service_url}/deploy_os/{reservation_id}").json()

    def wait_os_installation(self, reservation_id, *args, **kwargs):
        os_installation_status = self.get_os_installation_status(reservation_id)
        while os_installation_status["installation_status"] not in [
            "complete",
            "failed",
        ]:
            os_installation_status = self.get_os_installation_status(reservation_id)
        return os_installation_status

    def get_resource_status(self, resource_model, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.get(
                f"{self.service_url}/resource/{resource_model}",
                json={
                    "resource": resource_model,
                    "is_reserved": True,
                    "os_installation": "complete",
                },
            )
            return requests.get(f"{self.service_url}/resource/{resource_model}").json()

    def get_active_user_reservations(self, user_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.delete(
                f"{self.service_url}/reservations/user/{user_id}",
                json={
                    "active_reservations": [
                        str(uuid4()) for _ in range(random.randint(1, 3))
                    ]
                },
            )
            return requests.delete(
                f"{self.service_url}/reservations/user/{user_id}"
            ).json()
