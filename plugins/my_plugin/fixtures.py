import os
import random

import pytest

from plugins.my_plugin.wrappers import ExampleProduct, SampleProduct


@pytest.fixture(scope="session")
def product():
    if os.getenv("TARGET_PRODUCT") == "example":
        return ExampleProduct("https://www.example.com")
    elif os.getenv("TARGET_PRODUCT") == "sample":
        return SampleProduct("https://www.sample.com")
    else:
        raise ValueError(f"Unexpected product configured {os.getenv('TARGET_PRODUCT')}")


@pytest.fixture(scope="session")
def admin_user(product):
    user_data = product.create_new_admin_user_session()["response"]
    if os.getenv("TARGET_PRODUCT") == "example":
        registration_response = product.register_admin_token(
            user_data["token"], user_data["user_id"]
        ).json()
        if not registration_response["response"]["registered"]:
            pytest.fail(f"Cant register user {user_data['user_id']=} as admin")
    return user_data


@pytest.fixture()
def create_reservation_config(product, admin_user):
    def factory(vendor, drives_type):
        available_resources = product.get_resources()
        target_server = next(
            server
            for server in available_resources["servers"]
            if server["manufacturer"] == vendor
        )
        required_drives = target_server["disk_count"]
        try:
            prepared_drives = random.choice(
                [
                    drive_type
                    for drive_type in available_resources["drives"]
                    if (drive_type["available"] >= required_drives)
                    and (drive_type["type"] == drives_type)
                ]
            )
        except IndexError:
            pytest.skip(f"Not enough drives for {required_drives=}")

        return {"server": target_server, "drives": prepared_drives}

    return factory


@pytest.fixture()
def create_reservation(product, admin_user, release_resources):
    def factory(reservation_config):
        reservation_data = product.reserve_resource(
            resource_config=reservation_config,
            user_data=admin_user,
        ).json()
        product.wait_deploy(
            reservation_data["reservation_id"], reservation_data["reserver_id"]
        )
        if os.getenv("TARGET_PRODUCT") == "sample":
            product.install_os(
                reservation_config,
                reservation_data["reservation_id"],
                product.get_available_os(filter={"name": "CentOS"}),
            )
        return reservation_data

    return factory


@pytest.fixture()
def release_resources(product, admin_user):
    yield
    active_user_reservations = product.get_active_user_reservations(
        admin_user["user_id"]
    )
    for reservation in active_user_reservations:
        product.release_resource(reservation, user_data=admin_user)


def pytest_runtest_teardown(item):
    print(f"pytest runtest teardown from plugin scope {os.getenv('TARGET_PRODUCT')}")
