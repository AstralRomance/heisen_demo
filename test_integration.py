import pytest
from plugins.my_plugin.assertions import StateAssertions


@pytest.mark.universal
@pytest.mark.parametrize("target_vendor", ["Tyan", "Fujitsu", "Dell"])
@pytest.mark.parametrize("drives_type", ["HDD", "SSD"])
def test_reservation_create(
    product, target_vendor, create_reservation_config, create_reservation, drives_type
):
    reservation_config = create_reservation_config(target_vendor, drives_type)
    reservation_data = create_reservation(reservation_config)
    assert reservation_data["reservation_id"]
    assert product.get_resource_status(reservation_config["server"]["model"])[
        "is_reserved"
    ]


@pytest.mark.universal
@pytest.mark.parametrize("target_vendor", ["Tyan", "Fujitsu", "Dell"])
@pytest.mark.parametrize("drives_type", ["HDD", "SSD"])
def test_reservation_create_compable_asserts(
    product,
    target_vendor,
    create_reservation_config,
    create_reservation,
    drives_type,
    assert_resource_reserved,
):
    reservation_config = create_reservation_config(target_vendor, drives_type)
    reservation_data = create_reservation(reservation_config)
    assert reservation_data["reservation_id"]
    StateAssertions.assert_resource_reserved(
        product.get_resource_status(reservation_config["server"]["model"])
    )
    assert_resource_reserved(
        product.get_resource_status(reservation_config["server"]["model"])
    )
