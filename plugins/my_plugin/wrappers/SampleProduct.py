import json
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
            return requests.get(f"{self.service_url}/resources")

    def reserve_resource(self, resource_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(
                f"{self.service_url}/reserve/{resource_id}",
                json={"reservation_id": str(uuid4())},
            )
            return requests.post(f"{self.service_url}/reserve/{resource_id}")

    def release_resource(self, resource_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(f"{self.service_url}/release/{resource_id}", json={})
            return requests.post(f"{self.service_url}/release/{resource_id}")
