from uuid import uuid4

import requests
import requests_mock

from plugins.my_plugin.wrappers.CommonProtocol import CommonProtocol


class SampleProduct(CommonProtocol):
    def __init__(self, root_url):
        self.service_url = root_url

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
            return requests.post(f"{self.service_url}/users/create_admin")

    def get_resources(self, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.get(f"{self.service_url}/resources", json={})
            return requests.get(f"{self.service_url}/resources")

    def reserve_resource(self, resource_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(f"{self.service_url}/reserve/{resource_id}", json={})
            return requests.post(f"{self.service_url}/reserve/{resource_id}")

    def release_resource(self, resource_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(f"{self.service_url}/release/{resource_id}", json={})
            return requests.post(f"{self.service_url}/release/{resource_id}")
