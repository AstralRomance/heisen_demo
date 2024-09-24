import pytest

import random


@pytest.mark.sample
@pytest.mark.parametrize("vendor", ["Tyan", "Fujitsu", "Dell"])
def test_sample_os_installation(
    product, create_sample_reservation, vendor, create_ssh_connection
):
    available_resources = product.get_resources()
    target_server = next(
        server
        for server in available_resources["servers"]
        if server["manufacturer"] == vendor
    )
    reservation_config = {
        "server": target_server,
        "drives": random.choice(
            [
                drive_type
                for drive_type in available_resources["drives"]
                if (drive_type["available"] >= target_server["disk_count"])
            ]
        ),
    }
    reservation_data = create_sample_reservation(reservation_config)
    product.install_os(
        reservation_config,
        reservation_data["reservation_id"],
        product.get_available_os(filter={"name": "Ubuntu Server"}),
    )
    installation_data = product.wait_os_installation(reservation_data["reservation_id"])
    assert installation_data["installation_status"] == "complete"
    deployed_resource_connection = create_ssh_connection(ip="111.111.11.11")
    assert deployed_resource_connection.get_os()
