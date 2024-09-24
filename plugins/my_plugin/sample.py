import os

import pytest

from plugins.my_plugin.wrappers import sshClient
from plugins.my_plugin.wrappers import SampleProduct


@pytest.fixture(scope="session")
def product():
    return SampleProduct("https://www.sample.com")


@pytest.fixture()
def create_sample_reservation(product):
    def factory(reservation_config):
        reservation_data = product.reserve_resource(
            resource_config=reservation_config,
            user_data=product.create_new_admin_user_session()["response"],
        ).json()
        product.wait_deploy(
            reservation_data["reservation_id"], reservation_data["reserver_id"]
        )
        return reservation_data

    return factory


@pytest.fixture()
def create_ssh_connection():
    def factory(
        ip,
        credentials={
            "username": os.getenv("SSH_USER", "sample"),
            "password": os.getenv("SSH_PASSWORD", "sample"),
        },
        *args,
        **kwargs
    ):
        return sshClient(ip=ip, credentials=credentials, *args, **kwargs)

    return factory
