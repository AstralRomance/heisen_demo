import requests
import requests_mock

from plugins.my_plugin.wrappers.CommonProtocol import CommonProtocol


class ExampleProduct(CommonProtocol):
    def __init__(self, root_url):
        self.service_url = root_url

    def get_data(self):
        with requests_mock.Mocker() as mock_request:
            mock_request.get(
                f"{self.service_url}/get_data",
                json={"response": "Response from Example mock"},
            )
            response = requests.get(f"{self.service_url}/get_data")
        return response

    def create_record(self, data):
        with requests_mock.Mocker() as mock_request:
            mock_request.post(
                f"{self.service_url}/create_record",
                json={"response": "Response from Example mock"},
            )
            response = requests.post(
                f"{self.service_url}/create_record", json=data
            )
        return response
