from uuid import uuid4

import requests
import requests_mock

from plugins.my_plugin.wrappers.CommonProtocol import CommonProtocol


class ExampleProduct(CommonProtocol):
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
                            "username": "example_admin",
                            "role": "admin",
                        },
                    }
                },
            )
            user = requests.post(f"{self.service_url}/users/create_admin").json()
            self.register_admin_token(user["response"].get("token"), user["response"].get("user_id"))
            return user

    def register_admin_token(self, token, user_id, *args, **kwargs):
        with requests_mock.Mocker() as mock_request:
            mock_request.update(
                f"{self.service_url}/userus/admin/register/{user_id}/{token}",
                json={"response": {"token": token, "registered": True}},
            )
            return requests.update(f"{self.service_url}/userus/admin/register/{user_id}/{token}")

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
